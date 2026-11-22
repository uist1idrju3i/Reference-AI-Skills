# MPIGの契約

固定版は[514497cfe184edda842f4410cd0eaee1acbdfb9c](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/README.md)です。日英12文書を読み、原文を転載せず契約を要約しました。各行のen・jaは固定commitの当該クラス文書です。戻り値・例外の「未規定」を、nilや特定の例外と読み替えません。optional parameterは原文の一覧と使用例に基づく名前であり、実装の引数解析方法を規定するものではありません。

## GPIO

| method | 引数・keyword・既定値・単位 | 戻り値 | 例外・条件・導入先が決める事項 | 出典 |
|---|---|---|---|---|
| .new(pin, params) | pin、modeのビットOR。省略値なし | GPIO | IN/OUT/HIGH_ZなしはArgumentError。型・排他・対応pinは導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| .setmode(pin, params) | constructorと同じ | nil | constructor参照。対応外の組合せは導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| .read_at(pin) | 1 pin | Integer 0/1 | 出力pinも可能なら実際の入力値。例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| .high_at?(pin) | 1 pin | bool、read値==1 | 例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| .low_at?(pin) | 1 pin | bool、read値==0 | 例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| .write_at(pin, integer_data) | 通常0/1 | 未規定 | 範囲外はRangeError。jaは複数bitの余地を残すがenは0/1を要求 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| #read() | 引数なし | Integer、通常0/1 | 複数bit実装だけ任意整数。例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| #high?() | 引数なし | bool、read値==1 | 例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| #low?() | 引数なし | bool、read値==0 | 例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| #write(integer_data) | 通常0/1、複数bit実装は任意整数 | 未規定 | instance側の例外は未規定。導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |
| #setmode(param) | modeのOR。方向指定で従来のpull設定を破棄 | nil | 例はPULL_UP単独の変更も含む。constructorの必須方向との適用差を導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_GPIO_ja.md) |

## ADC

| method | 引数・keyword・既定値・単位 | 戻り値 | 例外・条件・導入先が決める事項 | 出典 |
|---|---|---|---|---|
| .new(pin, *params) | 通常Integer pin、機種固有params、省略可 | ADC | 必要ならanalog modeへ変更。型・速度・対応pin・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_ja.md) |
| #read_voltage() | 引数なし、単位V | Float | Float無効ならNotImplementedError | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_ja.md) |
| #read() | read_voltageのalias、単位V | Float | Float無効ならNotImplementedError | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_ja.md) |
| #read_raw() | 引数なし、電圧換算前 | Integer | rawの範囲・分解能・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_ADC_ja.md) |

## PWM

| method | 引数・keyword・既定値・単位 | 戻り値 | 例外・条件・導入先が決める事項 | 出典 |
|---|---|---|---|---|
| .new(pin, *params) | frequency:/freq: Integer/Float Hz、duty: Integer/Float % | PWM | frequency指定時はduty省略で50%。frequencyなしは出力未開始。機器固有params・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_ja.md) |
| #frequency(freq) | Integer/Float Hz、0で停止 | 未規定 | dutyを保持。停止Lowが望ましい。周波数範囲・分解能・停止の周期境界・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_ja.md) |
| #period_us(micro_sec) | Integer μs、0で停止 | 未規定 | dutyを保持。負数・丸め・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_ja.md) |
| #duty(percent) | Integer/Float、0〜100 % | 未規定 | 範囲外の扱い・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_ja.md) |
| #pulse_width_us(micro_sec) | Integer μs | 未規定 | 周期超過は最大ONへ制限しエラーにしない。負数等は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_PWM_ja.md) |

## UART

| method | 引数・keyword・既定値・単位 | 戻り値 | 例外・条件・導入先が決める事項 | 出典 |
|---|---|---|---|---|
| .new(id=nil, *params) | baudrate:/baud: 9600 bps、data_bits:8、stop_bits:1、parity:NONE、flow_control:NONE。unit:はidと同義、txd_pin:/rxd_pin:/rts_pin:/cts_pin: | UART | 既定設定は可能な限り従う。pin・unit表現・対応parameter・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #setmode(*params) | constructorのparameterで再設定 | 未規定 | 省略parameterの保持/再初期化・競合alias・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #read(read_bytes) | 要求byte数、既定なし | String | 指定長まで待機。0・負数・上限・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #write(string) | Stringのbyte列 | Integer、送ったbyte数 | 送信完了より早く戻る場合あり。部分送信・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #gets() | LFまで、buffer容量が上限 | String | 行到着まで待機。LFなしで満杯の救済・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #puts(string) | 既定LF | nil | jaは末尾改行がなければ追加、enは末尾に追加とだけ記述。重複LFの扱いは導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #bytes_available() | 引数なし、単位byte | Integer | 現在の受信buffer量。確認後の競合・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #bytes_to_write() | 引数なし、単位byte | Integer | 未送信buffer量。bufferなしは0。例外は未規定 | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #can_read_line() | 引数なし | bool | 行読出し可能か。確認後の競合・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #flush() | 引数なし | 未規定 | 送信完了まで待機。timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #clear_rx_buffer() | 引数なし | 未規定 | 受信buffer破棄。実行中転送との競合・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #clear_tx_buffer() | 引数なし | 未規定 | 送信buffer破棄。既に送信中のbyte・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |
| #send_break(time) | 任意time、単位秒。既定数値は未規定 | 未規定 | 機器により時間固定。範囲・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_UART_ja.md) |

## I2C

| method | 引数・keyword・既定値・単位 | 戻り値 | 例外・条件・導入先が決める事項 | 出典 |
|---|---|---|---|---|
| .new(id=nil, *params) | frequency:/freq: Integer Hz、既定100 kHz。scl_pin:/sda_pin: | I2C | 単一unit等ではid省略可。master、7bit addressのみ。対応parameter・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #read(i2c_adrs_7, read_bytes, *param) | address、byte数、先行出力（writeと同じ形式） | String、NAK時は短くなりうる | 先行出力→repeated START→read。0長・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #write(i2c_adrs_7, *outputs) | Integer / Array<Integer> / Stringを混在 | Integer、書けたbyte数 | 範囲・空出力・NAK・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #send_start() | 任意実装のlow-level | 未規定 | START。例外・排他は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #send_restart() | 任意実装のlow-level | 未規定 | repeated START。例外・排他は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #send_stop() | 任意実装のlow-level | 未規定 | STOP。例外・排他は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #raw_read(read_bytes, ack_nack=false) | byte数、最後のbyteでtrueはACK・falseはNACK | String | 任意実装。0長・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |
| #raw_write(*outputs) | Integer / Array<Integer> / String | Integer、書けたbyte数 | 任意実装。空・範囲・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_I2C_ja.md) |

## SPI

| method | 引数・keyword・既定値・単位 | 戻り値 | 例外・条件・導入先が決める事項 | 出典 |
|---|---|---|---|---|
| .new(id=nil, *params) | unit:、frequency: Integer Hzで既定1 MHz、mode:0、first_bit:MSB_FIRST | SPI | master、8bit転送のみ。LSB_FIRSTあり。pin/unit表現・対応parameter・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_ja.md) |
| #setmode(*params) | constructorのparameterに準拠 | 未規定 | 省略parameterの保持・対応mode・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_ja.md) |
| #read(read_bytes) | 要求byte数、同時送信は0 | String | 0長・部分転送・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_ja.md) |
| #write(*outputs) | Integer / Array<Integer> / Stringを混在 | nil | 空・範囲・timeout・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_ja.md) |
| #transfer(outputs, additional_read_bytes=0) | 出力はInteger / Array<Integer> / String。追加byteは0で送信 | String、出力と追加byteの同時受信 | 追加長は位置引数。負数・空・部分転送・例外は導入先が決める | [en](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_en.md) / [ja](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/mruby_io_SPI_ja.md) |

## 導入先が決める事項

日英で契約上の記述差を確認したのはGPIO.write_atの複数bitへの余地とUART#putsの改行条件です。他のクラスではこの読み取りの範囲で意味上の差を見つけていません。差や曖昧さが残る場合は採用する解釈と理由を明示し、上流の規定と導入先の決定を分けます。

GPIOの定数はIN、OUT、HIGH_Z、PULL_UP、PULL_DOWN、OPEN_DRAINです。bit値や排他条件は本文に数値規定がありません。方向必須はconstructorに明記される一方、instanceのsetmode例はpullだけの更新を含みます。型と例外、競合するflagsの優先順位、未知bit、複数bitの対応は導入先が決めます。

UARTの定数名はNONE、EVEN、ODD、RTSCTSです。SPIの定数名はMSB_FIRST、LSB_FIRSTで、modeは0〜3です。SPIのCSはGPIO側で管理し、SPI classの標準契約に自動CSを加えません。

共通してpin/unitの表現、対応外の設定、alias同時指定、所有者、busy、最大転送長、timeout/cancel、部分転送、buffer寿命、releaseは導入先が決める事項です。標準methodの戻り値や単位を黙って変えず、追加keywordやmethodは拡張として記録します。ADCのFloat無効時、GPIOの必須mode、GPIO.write_atの範囲外など、明記された例外はこの裁量に含めません。

## 帰属とライセンス

このMPIG要約は原資料の翻案であり、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)に従います。変更内容は日本語による再構成、契約表への整理、日英差と未規定事項の注記です。上流による承認を意味しません。[固定版READMEのLicense](https://github.com/mruby/microcontroller-peripheral-interface-guide/blob/514497cfe184edda842f4410cd0eaee1acbdfb9c/README.md#license)にある帰属を保持します。

- Copyright (C) 2023 mruby forum committee.
- Copyright (C) 2023 Kyushu Institute of Technology.
- Copyright (C) 2023 Shimane IT Open-Innovation Center.

上流には独立したLICENSEファイルがなく、READMEのLicense節が許諾と帰属を示します。community libraryの紹介部分はその許諾の対象外です。本スキルのコードは原資料から転記せず作成し、リポジトリのBSD-3-Clauseに従います。
