#! /usr/bin/perl
# record.pl: 録音スクリプト
# 							sako shinji
#
# $Id: record.pl,v 1.2 2006/10/16 03:57:59 sako Exp $
#
$| = 1;
use File::Basename;

#  音声データ収録用スクリプト ver 2.0
#
#               ver.1.0  2003 05/18  HOSSY
#               ver.1.1  2004/08/11  sako shinji
#               ver.1.2  2004/09/09  sako shinji
#
#               ver.2.0  2005/08/03  sako shinji
#               ver.2.1  2006/03/14  sako shinji
#               ver.2.2  2006/08/01  sako shinji
#
#		ver (u-tokyo) sox 関連を修正 [ Daisuke Saito ]
# 設定ファイルのパス設定
$script_base = dirname( $0);
require $script_base . "/config.pl";
#
# 提示用サンプル音声データ
#

# 提示文章データ
$sentence_file = "${database}/sentence.txt";
# サンプル音声
$samplepath = "${database}/speech";

# 録音データ保存場所
$outpath = "${recdir}";

# julius 附属ツールで録音
# 前後のマージンを400ミリ秒として切り出す(adinrecの機能)
$record_command = "$adinrecbin -quiet -lv 1000 -freq 16000 -headmargin 400 -tailmargin 400 ";

# play (sox)コマンドで再生
# 上のフォーマットを指定して再生
#$play_command = "play ";

# 出力先ディレクトリの作成
if ( "${outpath}" ne "") {
	system "mkdir -p $outpath" || die "ディレクトリを作成できません ($outpath)";
}

sub help{
    print STDERR "\n [ 使い方 ]\n";
    print STDERR "  % の後にコマンド入力\n";
    print STDERR "  l   : 録音した音声を聞く\n";
    print STDERR "  r   : 録音する\n";
    print STDERR "  R   : 録音やり直し(お手本無し)\n";
    print STDERR "  t   : お手本を聞き直す\n";
    print STDERR "  b   : 前の文に戻る\n";
    print STDERR "  n   : 次の文へ進む\n";
    print STDERR "  m X : 文章 X へ移動（例:m b01）\n";
    print STDERR "  h   : このメッセージ\n";
    print STDERR "  q   : 終了\n";
    print STDERR "\n";
}

# 音声の再生
sub raw_play{
    my $audiofile = $_[0];
    if( -s "${audiofile}" ){
	system "$play_command ${audiofile} 2> /dev/null";
	#system "$play_command ${audiofile}";
    }
    else{
        print STDERR "ERROR: 音声データがありません ($audiofile)\n";
    }
}

# 音声の録音
sub raw_record{
    my $audiofile = $_[0];
    my $tmpfile = basename(${audiofile});
    system "${record_command} ${tmpfile} > /dev/null";
    system "mv ${tmpfile} ${audiofile}";
    if( -s "${audiofile}" ){
	;
    }
    else{
	print STDERR "ERROR: 録音に失敗しました ($audiofile)\n";
    }
}

# 
sub readfile{
    my $inputfile = $_[0];
    my @tmp_list=();
    
    open(TXT,$inputfile) || die "ERROR: ファイルを開けません ($inputfile)\n";
    while(<TXT>){
        chomp;
        my @s = split (':');
	my %tmphash = (num => $s[0], kanji => $s[1], kana => $s[2]);
	push (@tmp_list, \%tmphash); 
        #push (@tmp_list, {"num", $_[0], "kanji", $_[1], "kana", $_[2]});
    }
    close(TXT);
    
    return @tmp_list;
}

#
sub recinfo{
    my $t_num = $_[0];
    my $t_kanji = $_[1];
    my $t_kana = $_[2];
    
    print "\n\[${t_num}\]";
    if( -s "${outpath}/s${spkidx}_${t_num}.wav"){
	# ファイルの更新時刻を取得
	my @file_stat = stat( "${outpath}/s${spkidx}_${t_num}.wav");
	my $mtime = localtime( $file_stat[9]); 
	print " *録音済  ${outpath}/s${spkidx}_${t_num}.wav ($mtime)\n\n";
    }
    else{
	print " *未録音\n\n";
    }
    # 読み上げ文章を表示
    if( $t_kana )  {print "      $t_kana\n";}
    if( $t_kanji ) {print "      $t_kanji\n";}

    print("\n");
}

# 
@textset = readfile( $sentence_file);

#引き数読み込み
my $start;
if(@ARGV==1){
    $start = 0;
    $spkidx = $ARGV[0];
}
elsif(@ARGV==2){
    $spkidx = $ARGV[0];
    chomp($ARGV[1]);

    for( my $j = 0; $j < $#textset; $j++){
	if( $textset[$j]{"num"} eq $ARGV[1]){
	    $start = $j;
	}
    }
}
else{
    print "Usage: \$ ./record.pl [speaker index]\n実行時に話者番号を指定して下さい\n";
    exit 1;
}

help;

$i = $start;

while(){
    my $num = $textset[$i]{"num"};
    my $kanji = $textset[$i]{"kanji"};
    my $kana = $textset[$i]{"kana"};
    my $outputfile =  "${outpath}/s${spkidx}_${num}.wav";
    my $samplefile =  "${samplepath}/${num}.wav";

    recinfo( $num, $kanji, $kana);

    print "% ";
    $input = <STDIN>;

# help    
    if( $input eq ""){
	if( -s $outputfile){
	    $input = "n\n";
	}
	else{
	    $input = "r";
	}
    }
    if($input=~/^h/){
	help;
    }
# 録音した音声を再生	      
    elsif($input=~/^l/){
	# 
	raw_play( $outputfile);
    }
# 録音
    elsif($input=~/^r/){
	# 
	raw_play( $samplefile);
	raw_record( $outputfile);
    }
    elsif($input=~/^R/){
	raw_record( $outputfile);
    }   	
#
    elsif($input=~/^t/){
	# 
	raw_play( $samplefile);
    }
# 前の文章へ戻る
    elsif($input=~/^[bB]/){
	$i-=1;
	if( $i < 0){
	    $i=0;
	}
    }
# 終了
    elsif($input=~/^[qQ]/){
	printf "\n終了します\n";
	exit 0;
    }
# 次の文章へ
    elsif($input=~/^n/){
	$i=$i+1;
	if( $i > $#textset){
	    $i = $#textset;
	}
    }
# 特定の文章へ移動	      
    elsif($input=~/^m /){
				$moveto = $';
	chomp($moveto);
	my $j=0;
        for ($j=0; $j<=$#textset; $j++){
	    if( $textset[$j]{"num"} eq $moveto){
		$i = $j;
		next;
	    }
	}
    }
}
print "\n終了しました\n";
