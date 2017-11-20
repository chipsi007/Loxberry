#!/usr/bin/perl

# Copyright 2017 Michael Schlenstedt, michael@loxberry.de
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##########################################################################
# Modules
##########################################################################

use LoxBerry::System;
use LoxBerry::Web;

use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
use LWP::UserAgent;
use Config::Simple;
use warnings;
use strict;
no strict "refs"; # we need it for template system

##########################################################################
# Variables
##########################################################################

our $cfg;
our $phrase;
our $namef;
our $value;
our %query;
our $lang;
our $template_title;
our $help;
our @help;
our $helptext;
our $helplink;
#our $installfolder;
our $languagefile;
our $version;
our $error;
our $saveformdata;
our $checked1;
our $checked2;
our $checked3;
our $checked4;
our $netzwerkanschluss;
our $netzwerkssid;
our $netzwerkschluessel;
our $netzwerkadressen;
our $netzwerkipadresse;
our $netzwerkipmaske;
our $netzwerkgateway;
our $netzwerknameserver;
our $lbfriendlyname;
our @lines;
our $do;
our $message;
our $nexturl;
# our $lbhostname = lbhostname();

##########################################################################
# Read Settings
##########################################################################

# Version of this script
$version = "0.3.1-dev2";

print STDERR "============= network.cgi ================\n";
print STDERR "lbhomedir: $lbhomedir\n";



$cfg                = new Config::Simple("$lbsconfigdir/general.cfg");
#$installfolder      = $cfg->param("BASE.INSTALLFOLDER");
#$lang               = $cfg->param("BASE.LANG");
$netzwerkanschluss  = $cfg->param("NETWORK.INTERFACE");
#$netzwerkssid       = $cfg->param("NETWORK.SSID");
$netzwerkadressen   = $cfg->param("NETWORK.TYPE");
#$netzwerkipadresse  = $cfg->param("NETWORK.IPADDRESS");
#$netzwerkipmaske    = $cfg->param("NETWORK.MASK");
#$netzwerkgateway    = $cfg->param("NETWORK.GATEWAY");
#$netzwerknameserver = $cfg->param("NETWORK.DNS");
#$lbfriendlyname 	= $cfg->param("NETWORK.FRIENDLYNAME");


my $maintemplate = HTML::Template->new(
			filename => "$lbstemplatedir/network.html",
			global_vars => 1,
			loop_context_vars => 1,
			die_on_bad_params=> 0,
			associate => $cfg,
			);

LoxBerry::Web::readlanguage($maintemplate);

#########################################################################
# Parameter
#########################################################################

# Everything from URL
foreach (split(/&/,$ENV{'QUERY_STRING'})){
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# And this one we really want to use
$do           = $query{'do'};

# Everything we got from forms
$saveformdata         = param('saveformdata');
defined $saveformdata ? $saveformdata =~ tr/0-1//cd : undef;
print STDERR "saveformdata: $saveformdata\n";
print STDERR "do querystring: $do\n";

##########################################################################
# Language Settings
##########################################################################

$lang = lblanguage();
print STDERR "Language in network: $lang\n";
$maintemplate->param( "LBHOSTNAME", lbhostname());
$maintemplate->param( "LANG", $lang);
$maintemplate->param ( "SELFURL", $ENV{REQUEST_URI});

#our $navbar ="<p>Hello</p>";

our %navbar;
$navbar{1}{Name} = "First Menu";
$navbar{1}{URL} = '#';
$navbar{1}{target} = '_blank';

$navbar{2}{Name} = "Second Menu";
$navbar{2}{URL} = '#';
$navbar{2}{active} = 1;

$navbar{3}{Name} = "External Website";
$navbar{3}{URL} = 'http://www.loxberry.de';
$navbar{3}{target} = '_blank';


##########################################################################
# Main program
##########################################################################

#########################################################################
# What should we do
#########################################################################

# Step 1 or beginning
if (!$saveformdata) {
  print STDERR "FORM called\n";
  $maintemplate->param("FORM", 1);
  &form;
} else {
  print STDERR "SAVE called\n";
  $maintemplate->param("SAVE", 1);
  &save;
}

exit;

#####################################################
# Form
#####################################################

sub form {

# Defaults for template
if ($netzwerkanschluss eq "eth0") {
  $maintemplate->param( "CHECKED1", 'checked="checked"');
} else {
  $maintemplate->param( "CHECKED2", 'checked="checked"');
}

if ($netzwerkadressen eq "manual") {
  $maintemplate->param( "CHECKED4", 'checked="checked"');
} else {
  $maintemplate->param( "CHECKED3", 'checked="checked"');
}

# Print Template
print STDERR "lbfriendlyname before output: $lbfriendlyname\n";
$template_title = $lbfriendlyname . " " . $SL{'COMMON.LOXBERRY_MAIN_TITLE'} . ": " . $SL{'NETWORK.WIDGETLABEL'};
LoxBerry::Web::head();

LoxBerry::Web::pagestart(undef, "http://www.loxwiki.eu/display/LOXBERRY/LoxBerry", "network.html");

print $maintemplate->output();
undef $maintemplate;			

LoxBerry::Web::pageend();

LoxBerry::Web::foot();

exit;

}

#####################################################
# Save
#####################################################

sub save {

# Everything from Forms
$netzwerkanschluss  = param('netzwerkanschluss');
$netzwerkssid       = param('netzwerkssid');
$netzwerkschluessel = param('netzwerkschluessel');
$netzwerkadressen   = param('netzwerkadressen');
$netzwerkipadresse  = param('netzwerkipadresse');
$netzwerkipmaske    = param('netzwerkipmaske');
$netzwerkgateway    = param('netzwerkgateway');
$netzwerknameserver = param('netzwerknameserver');
$lbfriendlyname	    = param('lbfriendlyname');
print STDERR "lbfriendlyname before SAVE: $lbfriendlyname\n";

# Write configuration file(s)
$cfg->param("NETWORK.INTERFACE", "$netzwerkanschluss");
$cfg->param("NETWORK.SSID", "$netzwerkssid");
$cfg->param("NETWORK.TYPE", "$netzwerkadressen");
$cfg->param("NETWORK.IPADDRESS", "$netzwerkipadresse");
$cfg->param("NETWORK.MASK", "$netzwerkipmaske");
$cfg->param("NETWORK.GATEWAY", "$netzwerkgateway");
$cfg->param("NETWORK.DNS", "$netzwerknameserver");
$cfg->param("NETWORK.FRIENDLYNAME", "$lbfriendlyname");

$cfg->save();

# Set network options
# Wireless
if ($netzwerkanschluss eq "wlan0") {

  # Manual / Static
  if ($netzwerkadressen eq "manual") {
    open(F1,"$lbhomedir/system/network/interfaces.wlan_static") || die "Missing file: $lbhomedir/system/network/interfaces.wlan_static";
     open(F2,">$lbhomedir/system/network/interfaces") || die "Missing file: $lbhomedir/system/network/interfaces";
      flock(F2,2);
      while (<F1>) {
        $_ =~ s/<!--\$(.*?)-->/${$1}/g;
        print F2 $_;
      }
      flock(F2,8);
     close(F2);
    close(F1);

  # DHCP
  } else {
    open(F1,"$lbhomedir/system/network/interfaces.wlan_dhcp") || die "Missing file: $lbhomedir/system/network/interfaces.wlan_dhcp";
     open(F2,">$lbhomedir/system/network/interfaces") || die "Missing file: $lbhomedir/system/network/interfaces";
      flock(F2,2);
      while (<F1>) {
        $_ =~ s/<!--\$(.*?)-->/${$1}/g;
        print F2 $_;
      }
      flock(F2,8);
     close(F2);
    close(F1);
  }

# Ethernet
} else {

  # Manual / Static
  if ($netzwerkadressen eq "manual") {
    open(F1,"$lbhomedir/system/network/interfaces.eth_static") || die "Missing file: $lbhomedir/system/network/interfaces.eth_static";
     open(F2,">$lbhomedir/system/network/interfaces") || die "Missing file: $lbhomedir/system/network/interfaces";
      flock(F2,2);
      while (<F1>) {
        $_ =~ s/<!--\$(.*?)-->/${$1}/g;
        print F2 $_;
      }
      flock(F2,8);
     close(F2);
    close(F1);

  # DHCP
  } else {
    open(F1,"$lbhomedir/system/network/interfaces.eth_dhcp") || die "Missing file: $lbhomedir/system/network/interfaces.eth_dhcp";
     open(F2,">$lbhomedir/system/network/interfaces") || die "Missing file: $lbhomedir/system/network/interfaces";
      flock(F2,2);
      while (<F1>) {
        $_ =~ s/<!--\$(.*?)-->/${$1}/g;
        print F2 $_;
      }
      flock(F2,8);
     close(F2);
    close(F1);
  }
}

print "Content-Type: text/html\n\n";
$template_title = $lbfriendlyname . " " . $SL{'COMMON.LOXBERRY_MAIN_TITLE'} . ": " . $SL{'NETWORK.WIDGETLABEL'};
$help = "network";

$maintemplate->param("NEXTURL", "/admin/index.cgi");

# Print Template
LoxBerry::Web::head();
LoxBerry::Web::pagestart();
print $maintemplate->output();
LoxBerry::Web::pageend();
LoxBerry::Web::foot();
exit;

}

exit;


#####################################################
# 
# Subroutines
#
#####################################################

#####################################################
# Error
#####################################################

sub error {

$template_title = $lbfriendlyname . " " . $phrase->param("TXT0000") . " - " . $phrase->param("TXT0028");
$help = "network";

print "Content-Type: text/html\n\n";

LoxBerry::Web::head();
LoxBerry::Web::pagestart();

open(F,"$lbhomedir/templates/system/$lang/error.html") || die "Missing template system/$lang/error.html";
    while (<F>) {
      $_ =~ s/<!--\$(.*?)-->/${$1}/g;
      print $_;
    }
close(F);

LoxBerry::Web::pageend();
LoxBerry::Web::foot();

exit;

}


