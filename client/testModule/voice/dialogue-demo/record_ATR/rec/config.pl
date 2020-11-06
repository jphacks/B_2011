# config_ini.pl: 学習データの収録，作成のための初期設定ファイル
#
# * 酒向先生のVoiceMaker のスクリプトをもとに作成
# by Daisuke Saito ( The University of Tokyo)
#
#
# このファイル(config.pl)のあるディレクトリを指定
# 
# あらゆるファイルのパスの起点になるため，途中で変更した場合は
# パスの構造のミスマッチによるエラーが生じる可能性があるため注意
use Cwd;
use File::Basename;
$base=getcwd;

# 話者名(任意の文字列)
$speaker="test";
# 未設定の場合はユーザ名を使用
if( $speaker eq ""){
	$speaker=$ENV{USER};
}

# Julius / adinrec の実行パス
$juliusbin  = "julius";
$adinrecbin = "adinrec"; 

# Play (sox) の実行パス
$play_command = "play -q"; 

# 以下，基本的には変更不要
#
# データベースの雛型のパス
$database="${base}/reference";

# 作成する学習データのパス
# ここより下に学習で必要なデータが作成される

# 音声データ収録ディレクトリ
$recdir="../wav";
if( ! -d $recdir ) {
    mkdir $recdir, 0755;
}

# 収録する音声データのサンプルレート (Hz)
# (原則として固定)
$samplerate=16000;

