#!/usr/bin/perl
# segment.pl: Juliusを利用したセグメンテーションツール
#
# $Id: segment.pl,v 1.2 2006/10/16 03:57:59 sako Exp $
#
# perform forced alignment using Julian
#
# usage: segment_julian.pl speechfile transfile
#
# output will be written to 'trans.align', and
# Julian log will be stored in 'trans.log'
#

######################################################################
######################################################################
#### user configuration
use File::Basename;
$script_base = dirname( $0);

require $script_base . '/config.pl';

## julian executable
# $julianbin="julius";
$julianbin = $juliusbin;

## acoustic model
$hmmdefs=$script_base . "/hmmdefs_monof_mix16_gid.binhmm";

## HMMList file (needed if above is triphone based model)
#$hlist="/somewhere/IPA99/phone_m/parms/logicalTri.added";

## working directory
#$TMPDIR="${tmpdir}";
$TMPDIR= $script_base . "/tmp";
if( ! -d $TMPDIR ) {
    mkdir $TMPDIR, 0755;
}


## other options to Julian
$OPTARGS="-quiet  -input rawfile";	# raw speech file input
#$OPTARGS="-input mfcfile";	# MFCC file input

## enable debug message
$debug_flag=0;			# set to 1 for debug output to speechfile.log
$julianlog="${TMPDIR}/julian.log";

######################################################################
######################################################################

#### initialize
if ($#ARGV < 1) {
    print "usage: segment.pl speech_file trans_file\n";
    exit;
}
$speechfile = $ARGV[0];
$transfile  = $ARGV[1];
$logfile = $ARGV[2];

$transfilelog = ${TMPDIR} . "/" . basename($ARGV[1]) . ".log";

if (! -r $speechfile) {
    die "Error: cannot open speech file \"$speechfile\"\n";
}
if (! -r $transfile) {
    die "Error: cannot open trans. file \"$transfile\"\n";
}

#### open result file for writing
open(RESULT, ">$logfile") || die "Error: cannot open result file \"$logfile\"\n";

#### generate speech grammar 'tmp.dfa' and 'tmp.dict' from transcription

# clean temporary file
unlink("$TMPDIR/tmp.dfa") if (-r "$TMPDIR/tmp.dfa");
unlink("$TMPDIR/tmp.dict") if (-r "$TMPDIR/tmp.dict");

## load .lab style transcription
open(TRANS0, "$transfile") || die "Error: cannot open transcription file";
@phoneme_list_hts=();
@phoneme_list_julius=();
while(<TRANS0>) {
	chomp;
	push(@phoneme_list_hts,$_);
	s/A/a/;
	s/I/i/;
	s/U/u/;
	s/E/e/;
	s/O/o/;
	s/cl/q/;
	s/pau/sp/;
	push(@phoneme_list_julius,$_);
}
@phoneme_list_julius[0] = "silB";
@phoneme_list_julius[$#phoneme_list_julius] = "silE";

## read transcription
#print RESULT "--- transcription ---\n";
@words=();
#open(TRANS, "$transfile") || die "Error: cannot open speech file \"$transfile\"\n";
#while(<TRANS>) {
#    chomp;
#    next if /^[ \t\n]*$/;
#    push(words, $_);
#    print RESULT "$_\n";
#}
push(@words, join( " ", @phoneme_list_julius));

#close(TRANS);
$num = $#words;

# write dfa
#print RESULT "--- generated DFA ---\n";
open(DFA, ">$TMPDIR/tmp.dfa") || die "Error: cannot open $TMPDIR/tmp.dfa for writing\n";
for ($i = 0; $i <= $num; $i++) {
    $str = sprintf("%d %d %d 0", $i, $num - $i, $i + 1);
    if ($i == 0) {
	$str .= " 1\n";
    } else {
	$str .= " 0\n";
    }
    print DFA "$str";
#    print RESULT "$str";
}
$str = sprintf("%d -1 -1 1 0\n", $num + 1);
print DFA "$str";
#print RESULT "$str";
close(DFA);

# write dict
#print RESULT "--- generated dict ---\n";
open(DICT, ">$TMPDIR/tmp.dict") || die "Error: cannot open $TMPDIR/tmp.dict for writing\n";
for ($i = 0; $i <= $num; $i++) {
    $w = shift(@words);
    $str = "$i [w_$i] $w\n";
    print DICT "$str";
#    print RESULT "$str";
}
### (ri) quick hack to avoid error in Julian 3.4 and 3.4.1...
if ($num == 0) {
    $str = "$num [w_$num] $w\n";
    print DICT "$str";
#    print RESULT "$str";
}
###
close(DICT);

#print RESULT "----------------------\n\n";

# check generated files
if ((! -r "$TMPDIR/tmp.dfa") || (! -f "$TMPDIR/tmp.dfa")) {
    die "Error: failed to make \"$TMPDIR/tmp.dfa\"\n";
}
if ((! -r "$TMPDIR/tmp.dict") || (! -f "$TMPDIR/tmp.dict")) {
    die "Error: failed to make \"$TMPDIR/tmp.dict\"\n";
}

#### execute Julian and store the output to log
#$command = "echo $speechfile | $julianbin -h $hmmdefs -dfa $TMPDIR/tmp.dfa -v $TMPDIR/tmp.dict";
$command = "echo $speechfile | $julianbin -fshift 80 -h $hmmdefs -dfa $TMPDIR/tmp.dfa -v $TMPDIR/tmp.dict";
if ($num > 0) {		# more than 1 line in trans
    $command .= " -walign";
}else{
    $command .= " -palign";
}

if ($hlist ne "") {
    $command .= " -hlist $hlist";
}
$command .= " $OPTARGS";
$command .= " -debug" if ($debug_flag != 0);

system("$command > ${transfilelog} 2>${julianlog}");

#### remove temporary file
unlink("$TMPDIR/tmp.dfa");
unlink("$TMPDIR/tmp.dict");

#### parse log and append result to speechfile.align
#print RESULT "============ ALIGNMENT RESULT ============\n";
$sw = 0;
@seg_result=();
open(LOG, "${transfilelog}") || die "Error: cannot open julian log file\n";
$line=0;
while(<LOG>){
    chomp;
    s/\r//;
    if (/^Stat:\s+adin_file:/){
	next;
    }
    if (/^STAT:\s+\d+\s+samples/){
	next;
    }
    if (/^=== begin forced alignment ===$/){
	$sw=1;
	next;
    }
    if ($sw == 1){
	if(/^\[[0-9, ]*/ && /[a-z,A-Z]$/){
	    # remove [ and ]
	    s/^\[/ /; s/\]/ /;
	    @item = split(/\s+/ , $_);
	    #printf RESULT "%d %d %s\n", 100000*$item[1],100000*($item[2]+1), $phoneme_list_hts[$line];
	    printf RESULT "%d %d %s\n", 50000*$item[1],50000*($item[2]+1), $phoneme_list_hts[$line];
	    #printf RESULT "%d %d %s\n", $item[1],$item[2], $phoneme_list_hts[$line];
	    $line++;
	    #print RESULT "$_\n";
	}
	#print RESULT "$_\n";
    }
    if (/^=== end forced alignment ===$/){
	$sw = 0;
    }
}
#while(<LOG>) {
#	chomp;
#	if( /^[0-9, ]*:/ && /[a-z,A-Z]$/){
#		@item = split( " ", $_);
#		printf RESULT "%d %d %s\n", 100000*$item[1],100000*($item[2]+1), $phoneme_list_hts[$line];
#		$line++;
#	}
#}


close(LOG);
close(RESULT);

#### end of processing
unlink( "${julianlog}");
unlink( "${transfilelog}");
# print "$score\n";
