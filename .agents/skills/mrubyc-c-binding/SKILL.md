---
name: mrubyc-c-binding
description: mruby/cにCのclass・methodを追加し、CからVMを扱う実装やレビューで使う。引数、戻り値、参照カウント、例外、taskの契約を固定版のソースとPOSIX fixtureで検証する。
---

# mruby/cのC binding

## 手順

1. mruby/cのcommit、mrbc、HAL、vm_configを記録します。[API契約表](references/api.md)はrelease4.0.0を対象とし、masterとの差分を分けています。mruby/CRubyのAPIをそのまま使えると仮定しません。
2. Ruby側のmethod、入力、空・未設定、出力、例外、副作用、資源のownerを先に決めます。Rubyで書ける制御はRubyへ置き、[mruby-idiomatic](../mruby-idiomatic/SKILL.md)に従います。Cは短い検査・native操作・値変換に絞ります。
3. 初期化、登録、task開始の順序を決めます。[登録とreceiver](references/api.md#登録とreceiver)でclass/instanceの境界を確認し、receiverの型とidentityも検査します。
4. [引数](references/api.md#引数)の位置を確認します。argc、kwargs、block、型、範囲をcastや副作用より前に検査します。省略とnilを分け、keywordのcleanupを成功・失敗の両経路に置きます。
5. 値ごとにownerを記録し、[所有権表](references/api.md#戻り値と所有権)でretain・移譲・借用を確かめます。`SET_RETURN`は古いselfをreleaseします。同じobjectを返す場合は返却分を先にretainし、移譲後に二度releaseしません。
6. [例外](references/api.md#例外とcからの呼出し)を設定したら、必要な後始末をしてreturnします。raiseがCの後続処理を止めると思わず、失敗後のdriver操作や成功値の設定を防ぎます。
7. Cから任意のRuby methodやblockを同期呼出しできると仮定しません。[mrbc_sendの制限](references/api.md#例外とcからの呼出し)を確認し、Ruby wrapperで開始・poll・block呼出し・ensureを組み立てます。
8. [taskとHAL](references/api.md#taskとhal)を確認し、長い処理は短い段階へ分けます。C callbackは有限時間で戻し、ISR/他threadの通知は同期した固定容量queueへ渡してforegroundで処理します。
9. destructor、明示release、task終了、VMID、pool全体の再初期化を別々に扱います。[寿命と版の注意](references/api.md#寿命と版の注意)に従い、shutdown時にC staticも整理します。objectのretainだけで依存先すべてが延命すると仮定しません。
10. [POSIXの自己検査](references/api.md#posixでの再現)を実行します。正常・空・型違い・不足・例外・destructor回数を検査し、compile成功だけで適合としません。対象版・設定が異なれば再実行し、実機でしか確かめられない事項を分けます。

## 参考にする実装

[RBOSとOpenBlinkの比較](references/patterns.md)は製品実装の観察です。上流APIの一般契約と混ぜず、error policy、所有者、reload単位を選ぶ材料にします。
周辺機器のMPIG契約、待機・timeout、fake GPIOには[mruby-common-io-api-guidelines](../mruby-common-io-api-guidelines/SKILL.md)を使います。

## 確認

- API契約、receiver、引数、例外、失敗後の副作用が一致している。
- 借用値の保存、self返却、containerへの移譲、取消し・shutdown時のreleaseを確認した。
- 同じschedulerの他taskを止める時間、queue上限、資源とbytecodeの寿命を決めた。
- 固定commitの根拠、fixtureの期待値、再現手順、結果、未検証事項を残した。
- 日本語、リンク、offline unittest、実行fixtureを検査した。

## 出所

APIは固定版ソースの独自要約、実例は[帰属付きの比較](references/patterns.md#帰属)です。第三者のbindingコードをコピーせず、独自fixtureで契約を検査します。
