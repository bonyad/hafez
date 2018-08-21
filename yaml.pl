#!/usr/bin/env perl

use strict;
use warnings;
use v5.012;
use utf8;

say "start  :(";

my $source = 'raw/*';
my @raws = glob ($source);

my $yaml = add_yaml_head();

foreach my $raw (@raws) {
	my ($num) = $raw =~ /(\d+)/;
	$num =~ s/^0+//;
	$yaml .= "  $num:\n";
	my $content = slurp_file($raw);
	$content =~ s/^/    - /mg;
	$yaml .= $content . "\n";
}

write_file($yaml);

say "finish :)";

sub slurp_file {
	my $file = shift;
	my $content;
	{
        open my $fh, '<:encoding(UTF-8)', $file or die $!;
        local $/ = undef;
        $content = <$fh>;
        close $fh;
    }
	$content =~ s/^[ \t]+$//mg;
	$content =~ s/\n+/\n/g;
	$content =~ s/\n+$//;
	return $content;
}

sub write_file {
	my $yaml = shift;
	open (my $fh, '>:encoding(UTF-8)', 'hafez.yaml') or die $!;
	print $fh $yaml;
	close $fh;
}

sub add_yaml_head {
return "HAFEZ: Collection of Hafez poems

Author: Bonyad (https://github.com/bonyad/)

Version: 0.1

Release date: 2018-08-21

License: http://creativecommons.org/licenses/by/4.0/

Introduction: >
  collection of Hafez poems in YAML format
  in order to be used by Persian free software community.

Resources:
  Hafez's page on English Wikipedia: https://en.wikipedia.org/wiki/Hafez
  Hafez's page on Farsi Wikipedia: https://fa.wikipedia.org/wiki/%D8%AD%D8%A7%D9%81%D8%B8

GHAZALIAT:
";
}
