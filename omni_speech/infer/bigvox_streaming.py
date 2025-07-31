import torch
import numpy as np
from omni_speech.model.builder import load_pretrained_model
from omni_speech.datasets.preprocess import preprocess_midm
import whisper
import argparse
from transformers import TextStreamer
# 체크포인트 경로 설정
BIGVOX_MODEL = "./checkpoints"

class BigVoxModel:
    def __init__(self, model_name_or_path: str, **kwargs):
        """s2t 추론을 위한 모델 초기화"""
        self.model_name_or_path = model_name_or_path
        self.empty = True

        # 생성 매개변수
        self.temperature = kwargs.get('temperature', 0.0)
        self.num_beams = kwargs.get('num_beams', 1)
        self.max_new_tokens = kwargs.get('max_new_tokens', 512)
        self.top_p = kwargs.get('top_p', 0.1)

    def __initialize__(self):
        """모델과 토크나이저 로드"""
        if self.empty:
            self.empty = False
            # s2s=False로 설정하여 s2t 전용 모델 로드
            
            self.tokenizer, self.model, _ = load_pretrained_model(self.model_name_or_path, s2s=False)
            self.suppress_tokens = []
            for i in range(len(self.tokenizer)):
                decoded = self.tokenizer.decode([i], skip_special_tokens=False, clean_up_tokenization_spaces=False)
                if '\x00' in decoded:
                    self.suppress_tokens.append(i)
    def __call__(self, messages: list) -> dict:
        """s2t 추론 수행"""
        # 입력 오디오 경로 가져오기
        audio_path = messages[0]['path']
        speech = whisper.load_audio(audio_path)
        
        # 오디오 전처리
        if self.model.config.speech_encoder_type == "glm4voice":
            speech_length = torch.LongTensor([speech.shape[0]])
            speech = torch.from_numpy(speech)
            speech = torch.nn.functional.layer_norm(speech, speech.shape)
        else:
            raw_len = len(speech)
            speech = whisper.pad_or_trim(speech)
            padding_len = len(speech)
            speech = whisper.log_mel_spectrogram(speech, n_mels=128).permute(1, 0).unsqueeze(0)
            speech_length = round(raw_len / padding_len * 3000 + 0.5)
            speech_length = torch.LongTensor([speech_length])
        
        # 대화 형식으로 입력 준비
        # The chat template expects a list of dicts with "role" and "content".
        conversation = [{"from": "human", "value": "<speech>", "path": f"{audio_path}"}]
        input_ids = preprocess_midm([conversation], self.tokenizer, True, 4096)['input_ids']
        input_ids = torch.cat([input_ids.squeeze(), torch.tensor([131302, 51728, 62350, 131303, 51613], device=input_ids.device)]).unsqueeze(0)
        attention_mask = torch.ones_like(input_ids)

        # 텐서를 GPU로 이동
        input_ids = input_ids.to(device='cuda', non_blocking=True)
        attention_mask = attention_mask.to(device='cuda', non_blocking=True)
        speech_tensor = speech.to(dtype=torch.float16, device='cuda', non_blocking=True)
        speech_length = speech_length.to(device='cuda', non_blocking=True)
        
        # 모델 추론
        streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        with torch.inference_mode():
            self.model.generate(
                input_ids,
                attention_mask=attention_mask,
                speech=speech_tensor,
                speech_lengths=speech_length,
                do_sample=True if self.temperature > 0 else False,
                temperature=self.temperature,
                top_p=self.top_p if self.top_p is not None else 0.0,
                num_beams=self.num_beams,
                max_new_tokens=self.max_new_tokens,
                use_cache=True,
                pad_token_id=2,
                eos_token_id=131301,
                suppress_tokens=self.suppress_tokens,
                streamer=streamer,
            )

if __name__ == "__main__":
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description='BigVox s2t inference')
    parser.add_argument('--query_audio', type=str, required=True, help='Path to the input audio file')
    args = parser.parse_args()

    # 메시지 준비
    audio_messages = [{"role": "user", "content": "<speech>", "path": args.query_audio}]
    print("Initialized BigVox for s2t")
    
    # 모델 초기화 및 추론
    bigvox = BigVoxModel(BIGVOX_MODEL)
    bigvox.__initialize__()
    bigvox(audio_messages)