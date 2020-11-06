#!/usr/bin/perl

$| = 1;
while (<STDIN>){
	if ( s/^sentence1: // ){
		s/silB//;
		s/silE//;
		s/ //g;
		print;
	}
}
