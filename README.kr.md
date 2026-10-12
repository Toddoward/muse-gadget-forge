[![English](https://img.shields.io/badge/lang-English-lightgrey?style=flat-square)](README.md)
[![한국어](https://img.shields.io/badge/lang-%ED%95%9C%EA%B5%AD%EC%96%B4-111111?style=flat-square)](README.kr.md)

# Muse Gadget Forge

**Gadget은 Muse에게 귀와 입을, Local Gateway는 손과 발을 줍니다.<br>
Forge는 작업대를 줍니다 — Muse가 다음 가젯을 직접 만드는 곳.**

[![License](https://img.shields.io/badge/license-Apache--2.0-111111?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-111111?style=flat-square)](CHANGELOG.md)
[![Community skill](https://img.shields.io/badge/Muse-community%20skill-lightgrey?style=flat-square)](#자주-묻는-질문)

ESP32를 컴퓨터에 꽂고 Muse에게 가젯을 부탁하세요. Muse가 펌웨어를 쓰고, ESP-IDF로 빌드하고, 책상 위 보드에
굽고, 시리얼 로그를 읽고, 깨진 곳을 고칩니다. 사용자가 터미널을 만지지 않아도 이 과정을 반복합니다.
그다음 Muse 앱에서 페어링하면, 보드는 Wi-Fi로 Muse와 혼자 대화합니다.

Forge는 [**Muse Local Gateway**](https://github.com/Toddoward/muse-local-gateway)의 추가 기능입니다. 게이트웨이의
격리된 셸을 ESP-IDF v6.0.1이 든 셸로 바꿉니다. 잠금장치도, 네트워크 모드도, 공유 폴더 하나도 그대로이고,
USB 보드만 더해집니다.

> 비공식 커뮤니티 프로젝트입니다. Muse 제작사와 관계가 없고 보증받지 않았습니다.

## 설치

1. [Muse Local Gateway](https://github.com/Toddoward/muse-local-gateway)를 설치하면서 USB 질문에 **y**라고 답합니다.
2. 이 저장소를 그 옆에 받고 설치 스크립트를 실행합니다(처음엔 ESP-IDF 약 5GB를 받습니다).

```bash
git clone https://github.com/Toddoward/muse-gadget-forge
./muse-gadget-forge/install.sh ./muse-local-gateway          # Linux
```

```powershell
git clone https://github.com/Toddoward/muse-gadget-forge
.\muse-gadget-forge\install.ps1 .\muse-local-gateway         # Windows
```

3. Muse에게: *"https://github.com/Toddoward/muse-gadget-forge 에서 muse_gadget_forge 스킬을 설치해 줘."*

`--remove`(Windows는 `-Remove`)로 빼면 원래 셸로 돌아갑니다.

## 보드

| 보드 | 나타나는 이름 | 빌드 | 굽기 |
|---|---|---|---|
| ESP32-S3, C3, C6 (네이티브 USB) | `/dev/ttyACM0` | ✅ ESP-IDF | ✅ |
| ESP32 DevKit (CP210x / CH340) | `/dev/ttyUSB0` | ✅ ESP-IDF | ✅ |
| ESP8266 (NodeMCU, D1 mini) | `/dev/ttyUSB0` | ❌ ESP-IDF 미지원 | ✅ 미리 빌드된 이미지 |

Linux와 Windows(usbipd-win 사용). macOS는 안 됩니다 — Docker Desktop이 USB를 넘기지 못합니다.

## Muse가 하는 일과 하지 않는 일

- 굽기 전에 묻습니다 — 보드에서 돌던 것이 바뀌기 때문입니다.
- 묻지 않고 플래시를 지우지 않습니다 — Wi-Fi 설정과 가젯 페어링이 사라지기 때문입니다.
- Gadget SDK 토큰은 사용자가 SDK 약관을 읽은 뒤 gadgets.muse.ai에서 직접 만듭니다.
- 페어링은 휴대폰의 Muse 앱에서 합니다. 컴퓨터는 작업대이지 중계기가 아닙니다. 페어링이 끝난 가젯은 컴퓨터가 필요 없습니다.

## 자주 묻는 질문

**공식 프로젝트인가요?** 아닙니다. 오픈소스 [Muse Gadget SDK](https://github.com/facebookincubator/muse-gadget-sdk)와
Muse Local Gateway 위에 만들었습니다.

**Gadget SDK를 쓰려면 꼭 필요한가요?** 아닙니다. 직접 구워도 됩니다. Forge는 빌드·굽기·디버깅 반복을 Muse가 스스로
하게 하려는 것입니다.

## 라이선스

[Apache-2.0](LICENSE). "Muse"는 해당 소유자의 상표이며, 무엇과 함께 동작하는지 밝히는 용도로만 씁니다.
