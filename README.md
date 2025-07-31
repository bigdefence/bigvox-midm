# 🎧 Bigvox

- **Bigvox**은 한국어 음성 인식에 특화된 고성능, 저지연 음성 언어 멀티모달 모델입니다. [K-intelligence/Midm-2.0-Mini-Instruct](https://huggingface.co/K-intelligence/Midm-2.0-Mini-Instruct) 기반으로 구축되었습니다. 🚀
- **End-to-End** 음성 멀티모달 구조를 채택하여 음성 입력부터 텍스트 출력까지 하나의 파이프라인에서 처리하며, 추가적인 중간 모델 없이 자연스럽게 멀티모달 처리를 지원합니다.


![image/png](https://cdn-uploads.huggingface.co/production/uploads/653494138bde2fae198fe89e/lpKXgUWIh7USbCOgSii-_.png)

### 📂 모델 접근
- **GitHub**: [bigdefence/bigvox-midm](https://github.com/bigdefence/bigvox-midm) 🌐
- **HuggingFace**: [bigdefence/Bigvox-Midm-Audio](https://huggingface.co/bigdefence/Bigvox-Midm-Audio) 🤗
- **모델 크기**: 2B 파라미터 📊

## 🌟 주요 특징

- **🇰🇷 한국어 특화**: 한국어 음성 패턴과 언어적 특성에 최적화
- **⚡ 경량화**: 2B 파라미터로 효율적인 추론 성능
- **🎯 고정확도**: 다양한 한국어 음성 환경에서 우수한 성능
- **🔧 실용성**: 실시간 음성 인식 애플리케이션에 적합

## 📋 모델 정보

| 항목 | 세부사항 |
|------|----------|
| **기반 모델** | K-intelligence/Midm-2.0-Mini-Instruct |
| **언어** | 한국어 (Korean) |
| **모델 크기** | ~2B 파라미터 |
| **작업 유형** | Speech-to-Text 음성 멀티모달 |
| **라이선스** | Apache 2.0 |

### 🔧 레포지토리 다운로드 및 환경 설정

**Bigvox**을 시작하려면 다음과 같이 레포지토리를 클론하고 환경을 설정하세요. 🛠️

1. **레포지토리 클론**:
   ```bash
   git clone https://github.com/bigdefence/bigvox-midm
   cd bigvox-midm
   ```

2. **의존성 설치**:
   ```bash
   bash setting.sh
   ```

### 📥 다운로드 방법

**Huggingface CLI 사용**:
```bash
pip install -U huggingface_hub
huggingface-cli download bigdefence/Bigvox-Midm-Audio --local-dir ./checkpoints
```

**Snapshot Download 사용**:
```bash
pip install -U huggingface_hub
```
```python
from huggingface_hub import snapshot_download
snapshot_download(
  repo_id="bigdefence/Bigvox-Midm-Audio",
  local_dir="./checkpoints",
  resume_download=True
)
```

**Git 사용**:
```bash
git lfs install
git clone https://huggingface.co/bigdefence/Bigvox-Midm-Audio
```

### 🛠️ 의존성 모델
- **Speech Encoder**: [Whisper-large-v3](https://huggingface.co/openai/whisper-large-v3) 🎤

### 🔄 로컬 추론

**Bigvox**으로 추론을 수행하려면 다음 단계를 따라 모델을 설정하고 로컬에서 실행하세요. 📡

1. **모델 준비**:
   - [HuggingFace](https://huggingface.co/bigdefence/Bigvox-Midm-Audio)에서 **Bigvox** 다운로드 📦
   - [HuggingFace](https://huggingface.co/openai/whisper-large-v3)에서 **Whisper-large-v3** 음성 인코더를 다운로드하여 `./models/speech_encoder/` 디렉토리에 배치 🎤

2. **추론 실행**:
   - **음성-텍스트(S2T)** 추론:
     ```bash
     python3 omni_speech/infer/bigvox.py --query_audio test_audio.wav
     ```
     ```bash
     python3 omni_speech/infer/bigvox_streaming.py --query_audio test_audio.wav
     ```

## 🔧 훈련 세부사항

### 데이터셋
- **VoiceAssistant**: 한국어 대화 음성 데이터

### 훈련 설정
- **Base Model**: K-intelligence/Midm-2.0-Mini-Instruct
- **Hardware**: 1x NVIDIA RTX 6000A GPU
- **Training Time**: 12시간

## ⚠️ 제한사항

- 배경 소음이 심한 환경에서는 성능이 저하될 수 있습니다
- 매우 빠른 발화나 중얼거리는 말투에 대해서는 인식률이 떨어질 수 있습니다
- 전문 용어나 고유명사에 대한 인식률은 도메인에 따라 차이가 있을 수 있습니다

## 📜 라이선스

이 모델은 Apache 2.0 라이선스 하에 배포됩니다. 상업적 사용이 가능하며, 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.


## 📞 문의사항

- **개발**: BigDefence

## 📈 업데이트 로그

### v1.0.0 (2024.12)
- 🎉 **초기 모델 릴리즈**: Bigvox 공개
- 🇰🇷 **한국어 특화**: K-intelligence/Midm-2.0-Mini-Instruct 기반 한국어 음성-텍스트 음성 멀티모달 모델
---

## 🤝 기여하기

**Bigvox** 프로젝트에 기여하고 싶으시다면:
---

**BigDefence**와 함께 한국어 AI 음성 인식의 미래를 만들어가세요! 🚀🇰🇷

*"Every voice matters, every word counts - 모든 목소리가 중요하고, 모든 말이 가치 있습니다"*
