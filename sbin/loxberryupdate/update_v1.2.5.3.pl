#!/usr/bin/perl

# Input parameters from loxberryupdate.pl:
# 	release: the final version update is going to (not the version of the script)
#   logfilename: The filename of LoxBerry::Log where the script can append
#   updatedir: The directory where the update resides
#   cron: If 1, the update was triggered automatically by cron

use LoxBerry::System;
use LoxBerry::Log;
use CGI;

my $cgi = CGI->new;
 

# Initialize logfile and parameters
	my $logfilename;
	if ($cgi->param('logfilename')) {
		$logfilename = $cgi->param('logfilename');
	}
	my $log = LoxBerry::Log->new(
			package => 'LoxBerry Update',
			name => 'update',
			filename => $logfilename,
			logdir => "$lbslogdir/loxberryupdate",
			loglevel => 7,
			stderr => 1,
			append => 1,
	);
	$logfilename = $log->filename;

	if ($cgi->param('updatedir')) {
		$updatedir = $cgi->param('updatedir');
	}
	my $release = $cgi->param('release');

# Finished initializing
# Start program here
########################################################################

my $errors = 0;
LOGOK "Update script $0 started.";

LOGINF "Removing obsolete 127.0.1.1 entry from /etc/hosts";
system ('sed -i "/127\.0\.1\.1.*$/d" /etc/hosts');


$output = qx { ln -f -s $lbhomedir/sbin/sethosts.sh /etc/network/if-up.d/001hosts };
$exitcode  = $? >> 8;
if ($exitcode != 0) {
	LOGERR "Error creating symlink $lbhomedir/sbin/sethosts.sh /etc/network/if-up.d/001hosts - Errorcode $exitcode";
	LOGDEB $output;
	$errors++;
} else {
	LOGOK "Symlink /etc/network/if-up.d/001hosts created successfully";
}


$output = qx { ln -f -s $lbhomedir/sbin/sethosts.sh /etc/dhcp/dhclient-exit-hooks.d/sethosts };
$exitcode  = $? >> 8;
if ($exitcode != 0) {
	LOGERR "Error creating symlink $lbhomedir/sbin/sethosts.sh /etc/dhcp/dhclient-exit-hooks.d/sethosts - Errorcode $exitcode";
	LOGDEB $output;
	$errors++;
} else {
	LOGOK "Symlink /etc/dhcp/dhclient-exit-hooks.d/sethosts created successfully";
}



## If this script needs a reboot, a reboot.required file will be created or appended
LOGWARN "Update file $0 requests a reboot of LoxBerry. Please reboot your LoxBerry after the installation has finished.";
reboot_required("LoxBerry Update requests a reboot.");

LOGOK "Update script $0 finished." if ($errors == 0);
LOGERR "Update script $0 finished with errors." if ($errors != 0);

# End of script
exit($errors);


sub delete_directory
{
	
	require File::Path;
	my $delfolder = shift;
	
	if (-d $delfolder) {   
		rmtree($delfolder, {error => \my $err});
		if (@$err) {
			for my $diag (@$err) {
				my ($file, $message) = %$diag;
				if ($file eq '') {
					LOGERR "     Delete folder: general error: $message";
				} else {
					LOGERR "     Delete folder: problem unlinking $file: $message";
				}
			}
		return undef;
		}
	}
	return 1;
}
