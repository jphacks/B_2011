# SATORI

[![IMAGE ALT TEXT HERE](https://user-images.githubusercontent.com/11728101/98431076-b0c97080-20f5-11eb-8f8f-eae77f3b234e.png)](https://www.youtube.com/watch?v=G5rULR53uMk)

## 製品概要
SATORIは、ユーザーのプライバシーや通信環境に配慮した、オンライン試験カンニング防止プラットフォームを提供するサービスです。

### 背景(製品開発のきっかけ、課題等）
COVID-19の影響により様々な試験がオンライン化し、大学4年生である私たちは大学院入試やTOEFLなどで大きくその影響を受けました。オンライン試験を受ける中で、カンニングへの対応の甘さや、プライバシーの問題を強く感じました。また、複数台のカメラを試験中常にオンにしなければならないなど、通信環境にも大きく依存している点に問題意識を感じました。
そこで、私たちは、ユーザーのプライバシーや通信環境に配慮しつつ、カンニングを防止するアプリケーションの開発をしたいと考えました。



### 製品説明（具体的な製品の説明）
### 特長
#### 1. 特長1
ほとんどの処理をクライアント側で済ませ、サーバ側にはどのような不正をしている可能性があるかだけを通知するので、ユーザーのプライバシーは最大限守られます！

#### 2. 特長2
クライアント側でほとんどの処理を済ませることで、通信量が大幅に減らせ、通信帯域が狭い環境下でも不利益を被ることなく使用できます！

#### 3. 特長3
アクティブウインドウやブラウザのタブを監視することで、ユーザーが試験に関係のないアプリケーションを開いていたり、関係ないブラウザのタブを見ていないかを監視することができます！

#### 4. 特長4
試験中の受験者の視線を検出し、頻繁に関係ない方向を見ていないかを確認することができます！

#### 5. 特長5
試験中の受験者の顔を検出し、受験者がなりすましをしていないかを確認することができます！

#### 6. 特長6
試験中の音声を検出し、受験中に第三者の声がしないかを確認することができます！

### 解決出来ること
- プライバシーの担保

私たちの中には、実際にオンライン試験を受ける中で、デスクトップを共有させられたり、マウスの権限を取られたりなどの経験をし、気持ちよくない思いをした人がいます。似たような体験をした人は他にも多数いると思います。そこで、私たちはプライバシーに配慮しつつカンニング対策を行うため、ほとんどの処理をクライアント側でのみ行い、正常に受験している場合、サーバには受験中のデータは何も送りません。もし不正を検出した場合、どのような項目で不正を検知したかをサーバに送信するという機構をとっています。

- 通信帯域の大幅な削減

オンライン試験では、こちらの動きをリアルタイムで監視するため、クライアントは動画や音声のデータを送信し続ける必要がありました。なので、通信帯域が狭い環境下にいる人は通信量が非常に多いせいで、意図せずアプリケーションが落ちてしまうという事態が発生することがあります。しかし、アプリケーションが落ちた場合、意図的かに関わらずペナルティを課すオンライン試験も存在します。環境のせいで不利益を被ることがないよう、私たちは通信量を減らすべく、サーバには動画や音声データを送信せず、全てクライアント側でのみ処理する仕組みを実現しました。

- 様々なカンニング手法に対応可能

上記のように過度のカンニング対策を行う試験が存在するのに対して、Zoomのカメラでのみしかカンニング対策をしていない試験も存在しました。そこで、考えられうるカンニング対策をできる限り行うべく、アクティブウインドウ/タブの監視、音声による第三者の介入の監視、顔認識によるなりすましの監視、目線の監視をクライアント側で実装しました。

### 今後の展望
- 完全なクロスプラットフォーム化（機能によってこのOSは対応している・していないが少し分かれてしまっている）
- 音声の機械学習モデルをWindowsで動くようにする。
- UIの改善。
- その他考察はされているが期間の都合実装しきれなかったカンニング手法の対策。

### 注力したこと（こだわり等）
* オンライン試験ならではのカンニング手法の列挙およびその対策手法の考察

## 開発技術
### 活用した技術
#### フレームワーク・ライブラリ・モジュール
* django
* vue
* win32gui
* opencv
* electron


### 独自技術
#### ハッカソンで開発した独自機能・技術
* クリップボードやアクティブウィンドウの切り替えによるカンニング検知。

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）
* 
* 
