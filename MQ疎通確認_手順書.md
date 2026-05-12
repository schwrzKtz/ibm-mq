# IBM MQ インフラ疎通確認 手順書

**対象読者:** インフラ担当者  
**前提:** アプリケーション開発不要。IBM MQ付属コマンド（amqsput / amqsget）のみで実施。

---

## 1. 疎通確認の全体像

```
【新規側（こちら）】                【既存側（対向）】
  サーバー / クライアント  ──接続──  Queue Manager
                                       └─ Queue
```

疎通確認は以下3段階で実施します。

| フェーズ | 内容 | 担当 |
|---|---|---|
| ① ネットワーク疎通 | IPアドレス・ポートへの到達確認 | インフラ（双方） |
| ② MQ接続確認 | Channel・QueueManagerへの接続確認 | インフラ（こちら）|
| ③ メッセージ送受信確認 | amqsput/amqsget によるテストメッセージ | インフラ（こちら）|

---

## 2. 事前に対向から入手する情報

疎通確認を開始する前に、以下の情報を対向システムの担当者から入手してください。

### 2-1. 必須情報（接続パラメータ）

| 項目 | 内容 | 記入欄（対向から入手）|
|---|---|---|
| QueueManager名 | 接続先のQMgr名 | |
| ホスト名 / IPアドレス | MQリスナーが動くサーバー | |
| ポート番号 | MQリスナーのポート（デフォルト1414）| |
| Channel名 | 使用するServer-Connection Channel（SVRCONN）| |
| Queue名（送信用）| こちらが Put するキュー名 | |
| Queue名（受信用）| こちらが Get するキュー名（折り返し確認用）| |

### 2-2. セキュリティ要件確認

| 項目 | Yes / No | 備考 |
|---|---|---|
| TLS/SSL 必要か | | 証明書の交換要否 |
| MCA認証（ID/PW）必要か | | ユーザー名・パスワードの払い出し要否 |
| IP制限（ファイアウォール）あるか | | こちらのIPアドレスを連携する必要あり |

### 2-3. こちらから対向に連携する情報

| 項目 | 内容 |
|---|---|
| 送信元IPアドレス | ファイアウォール許可申請に使用 |
| Channel名（Sender側）| Server-to-Server接続の場合 |
| QueueManager名（新規側）| Server-to-Server接続の場合 |

---

## 3. フェーズ①：ネットワーク疎通確認

### 3-1. pingによる到達確認

```bash
# 対向サーバーへのICMP疎通
ping -c 4 <対向IPアドレス>
```

**期待結果:** パケットロスなしで応答があること

### 3-2. MQポートへの接続確認

```bash
# telnetによるポート疎通
telnet <対向IPアドレス> <ポート番号>

# telnetが使えない場合（Linux）
nc -zv <対向IPアドレス> <ポート番号>

# telnetが使えない場合（Windows）
Test-NetConnection -ComputerName <対向IPアドレス> -Port <ポート番号>
```

**期待結果:** 接続が確立されること（`Connected` または `open` と表示される）

> **ポイント:** このステップで失敗した場合はネットワーク・ファイアウォールの問題です。  
> MQの設定より先に、ネットワーク担当者と連携して解消してください。

---

## 4. フェーズ②：MQ接続確認

### 4-1. 接続パターンの選択

疎通確認の方式は接続形態によって異なります。

| パターン | 新規側の構成 | 使用Channel |
|---|---|---|
| **A: クライアント接続** | MQクライアントのみインストール | Server-Connection Channel（SVRCONN） |
| **B: Server-to-Server** | QueueManagerをインストール | Sender/Receiver Channel |

---

### パターンA：クライアント接続での確認

#### A-1. MQSERVER環境変数のセット

```bash
# Linux/Unix
export MQSERVER='<Channel名>/TCP/<対向IPアドレス>(<ポート番号>)'

# 例
export MQSERVER='MQ.SVRCONN/TCP/192.168.1.100(1414)'
```

```cmd
:: Windows
SET MQSERVER=<Channel名>/TCP/<対向IPアドレス>(<ポート番号>)
```

#### A-2. amqsputによるメッセージ送信テスト

```bash
# 書式
/opt/mqm/samp/bin/amqsput <Queue名> <QueueManager名>

# 例
/opt/mqm/samp/bin/amqsput TEST.QUEUE QMGR01
```

コマンド実行後、テキストを入力してEnter → 空行でEnterすると送信完了。

```
Sample AMQSPUT0 start
target queue is TEST.QUEUE
hello from infra test    ← ここにメッセージを入力してEnter
                         ← 空行でEnter
Sample AMQSPUT0 end
```

**期待結果:** `Sample AMQSPUT0 end` が表示されること（エラーなし）

#### A-3. amqsgetによるメッセージ受信テスト

```bash
# 書式（15秒待機）
/opt/mqm/samp/bin/amqsget <Queue名> <QueueManager名>

# 例
/opt/mqm/samp/bin/amqsget TEST.QUEUE QMGR01
```

**期待結果:** 送信したメッセージが表示されること

---

### パターンB：Server-to-Server Channel接続での確認

#### B-1. こちら側のQueueManager（新規）を起動

```bash
# QueueManagerの起動確認
dspmq

# 起動していない場合
strmqm <QueueManager名>
```

#### B-2. Channelの定義確認（runmqsc）

```bash
runmqsc <QueueManager名>
```

```mqsc
* Sender Channelの確認
DISPLAY CHANNEL(<Channel名>)

* Receiver Channelの確認（対向用）
DISPLAY CHANNEL(<Channel名>)

* Channel状態の確認
DISPLAY CHSTATUS(*)

* 終了
END
```

#### B-3. Sender Channelの開始

```bash
runmqsc <QueueManager名>
```

```mqsc
START CHANNEL(<Sender Channel名>)
END
```

#### B-4. Channel状態の確認

```bash
runmqsc <QueueManager名>
```

```mqsc
DISPLAY CHSTATUS(<Channel名>)
END
```

**期待結果:** `STATUS(RUNNING)` が表示されること

#### B-5. amqsput / amqsget によるメッセージ確認

パターンAの A-2、A-3 と同様の手順で実施（ただしQueueManager名はこちら側のQMgr名を指定）。

---

## 5. フェーズ③：往復メッセージ確認（折り返し確認）

対向システムが折り返し（Request-Reply）に対応できる場合に実施します。

```
【こちら（新規）】           【対向（既存）】
  amqsput → SEND.QUEUE  →  受信キューに届く
  amqsget ← REPLY.QUEUE ←  対向が折り返し送信
```

| ステップ | コマンド（こちら側）| 確認内容 |
|---|---|---|
| 1. メッセージ送信 | `amqsput SEND.QUEUE QMGR01` | 対向担当者がキューで受信を確認 |
| 2. 対向が折り返し送信 | ─ | 対向担当者が REPLY.QUEUE に Put |
| 3. メッセージ受信 | `amqsget REPLY.QUEUE QMGR01` | こちらでメッセージ取得を確認 |

---

## 6. エラー発生時の切り分け

### よくあるエラーと対処

| エラーコード | エラーメッセージ | 原因 | 対処 |
|---|---|---|---|
| AMQ9204 | Connection to host refused | ポート未開放 / リスナー未起動 | フェーズ①を再確認。対向のリスナー起動確認 |
| AMQ9213 | Channel name error | Channel名が一致しない | 対向から正式なChannel名を再確認 |
| AMQ9503 | Channel stopped | Channel定義の不一致（TLS等）| TLS設定・Cipher要件を対向と合わせる |
| AMQ2035 | Not authorized | 認証エラー | ID/PWまたはMCA認証設定を確認 |
| AMQ9999 | Channel program ended abnormally | 一般エラー | MQエラーログ（/var/mqm/errors/）を確認 |

### ログ確認場所

```bash
# MQエラーログ（Linux）
cat /var/mqm/errors/AMQERR01.LOG | tail -100

# QueueManager固有のエラーログ
cat /var/mqm/qmgrs/<QueueManager名>/errors/AMQERR01.LOG | tail -100
```

---

## 7. 疎通確認エビデンスシート

疎通確認完了後、以下をエビデンスとして記録・保存してください。

### 7-1. 実施記録

| 項目 | 内容 |
|---|---|
| 実施日時 | |
| 実施者 | |
| 対向担当者 | |
| 環境 | 本番 / ステージング / 開発 |

### 7-2. 確認結果チェックリスト

| フェーズ | 確認項目 | 結果 | エビデンス（コマンド出力） |
|---|---|---|---|
| ① | ping 疎通 | OK / NG | |
| ① | ポート（1414）疎通 | OK / NG | |
| ② | MQ Channel 接続確立 | OK / NG | |
| ② | amqsput 送信成功 | OK / NG | |
| ② | amqsget 受信成功 | OK / NG | |
| ③ | 往復メッセージ確認 | OK / NG / 対象外 | |

### 7-3. コマンド出力の貼り付け

疎通確認コマンドの実行結果をそのまま貼り付けてください。

```
（ここにコマンドと出力結果を貼り付け）
```

---

## 8. 疎通確認前後の対向への依頼事項まとめ

### 疎通確認前（対向へ依頼）

- [ ] 接続パラメータ（QMgr名・ホスト・ポート・Channel名・Queue名）の提供
- [ ] ファイアウォール開放（こちらのIPアドレスを連携）
- [ ] MQリスナーの起動確認
- [ ] テスト用キューの払い出し（amqsput/amqsget用）
- [ ] 認証情報の払い出し（必要な場合）

### 疎通確認当日（対向に立ち会いを依頼）

- [ ] Channel・リスナーの状態監視（対向MQ管理者）
- [ ] こちらからのメッセージ着信確認（対向側でキューを監視）
- [ ] 折り返しメッセージの送信（往復確認の場合）

### 疎通確認後（対向へ連絡）

- [ ] 確認結果の共有
- [ ] 本番向け設定変更が必要な場合の調整

---

*本資料はインフラ担当レベルでの疎通確認を目的としています。アプリケーション結合試験は別途、開発担当者と実施してください。*
