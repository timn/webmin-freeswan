#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module Library
#    Copyright (C) 1999-2000 by Tim Niemueller <tim@niemueller.de>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    Created  : 16.09.2000

do '../web-lib.pl';
$|=1;
&init_config();
&ReadParse();
our %access=&get_module_acl;
our $cl=$text{'config_link'};
our $version="0.83.1-pre1";

our $ipsec_conf=($config{'conf'}) ? $config{'conf'} : "/etc/ipsec.conf";
our $ipsec_secrets=($config{'sec'}) ? $config{'sec'} : "/etc/ipsec.secrets";
our $ipsec_comm=($config{'ipseccomm'}) ? $config{'ipseccomm'} : &get_ipseccomm();
our @act=();   # For caching

# Check if FreeS/WAN is supported on the system
&error_setup($text{'lib_err'});

&error($text{'lib_err_nosupport'}) if (! -e "/proc/net/ipsec_version");
&error(&text('lib_err_nocomm', "<A HREF=\"/config.cgi?$modulename\">$text{'lib_modconf'}</A>")) if (! defined($ipsec_comm));


# parse_config()
# Parse the config file
sub parse_config {
  my $lines=&read_file_lines($ipsec_conf);
  my $secnms="config|conn";                # Section names
  my @rv=();                               # Return value
  my $cursec=undef;                        # Current section

  print "<HR><BR>" if $_DEBUG;
  for (my $i=0; $i < @$lines; $i++) {
    my $line=$lines->[$i];                            # For my lazyness and to prevent BadBugs (TM)
    # print "$_<BR>\n" if $_DEBUG;
    chomp $line;
    $line =~ s/^\s+//;                                # Remove whitespaces at line begin
    next if (($line =~ /^#/) || ($line eq ""));            # We ignore comments and blank lines

    if ($line =~ /^($secnms)/) {
      # we start a new section
      
      if (defined($cursec)) {
        # Go back until no more comments and blank lines
        my $j = $i-1;
        my $tmpline = $lines->[$j];
        chomp $tmpline;
        $tmpline =~ s/^\s+//;                                # Remove whitespaces at line begin
        while( ($tmpline =~ /^#/) || ($tmpline eq "")) {
          $tmpline = $lines->[--$j];
          chomp $tmpline;
          $tmpline =~ s/^\s+//;                                # Remove whitespaces at line begin
        }
        print "$line: $j<BR>\n" if $_DEBUG;
        $cursec->{'end__line'} = $j;       # define end if current sec is defined
      }
      my %directives=();
      $cursec = \%directives;                # Set current section
      push(@rv, $cursec);
      $line =~ /^($secnms){1}\s(\S+)+/;               # Get type and name of section
      $cursec->{'sectiontype'} = $1;
      $cursec->{'name'} = $2;
      ($cursec->{'name'} =~ /^(%default|[a-zA-Z][a-zA-Z0-9._-]*)$/) ||
         &error(&text('lib_err_syn', $cursec->{'name'}, $i+1));
      $cursec->{'start__line'} = $i;
    } else {
      # we add a directive to
      # we do not check if the directive is really valid, because this is
      # not _confread... But invalid settings will just be ignored in the
      # module

      $line =~ s/^\t+//;                                # Remove tabs at line begin
      $line =~ /^([a-zA-Z0-9._-]+){1}\s*=([\s\S]+){1}/;
      $cursec->{$1}=$2;
      $cursec->{"$1__line"}=$i;
    }
    if ($i == scalar(@$lines)-1) {
      # Go back until no more comments and blank lines
      # to get end__line of last section
      my $j = $i-1;
      while( ($lines->[$j] =~ /^#/) || ($lines->[$j] eq "")) {
        $j--;
      }
      $cursec->{'end__line'} = $j;       # define end if current sec is defined
    }
  }

return @rv;
}


# get_ipseccomm()
#
# Tries to determine the ipsec command

sub get_ipseccomm {

  return 'ipsec' if (&has_command('ipsec'));
  
  foreach $file ("/usr/local/sbin/ipsec", "/usr/sbin/ipsec",
                 "/sbin/ipsec") {
    return $file if (-x $file);
  }

return undef;
}



# get_conns(\parsed_conf)
# Returns an arraw with the names of connections
sub get_conns {

  my @rv=();
  foreach (@{$_[0]}) {
    if (($_->{'sectiontype'} eq 'conn') && ($_->{'name'} ne '%default')) {
      push(@rv, $_->{'name'});
    }
  }

return @rv;
}


# get_ipsecifcs()
# Returns an array with the names of available IPSEC interfaces
sub get_ipsecifcs {

  my @rv=();

  open(FILE, "/proc/net/ipsec_tncfg");
   my @lines=<FILE>;
  close(FILE);

  foreach (@lines) {
    /^(\S+){1}\s/;
    push(@rv, $1);
  }

return @rv;
}


# get_iface_select([devicename], [selectname])
# returns the HTML code for an device selectbox with devicename checked and
# the box named selectname
sub get_iface_select {
 my $sel = $_[0];
 my $selname = ($_[1]) ? $_[1] : "dev";

 my $rv = "<SELECT NAME=\"$selname\">\n";
 $rv .= "<OPTION VALUE=\"\">$text{'lib_noifc'}\n";



 if (!$config{'netifaces'}) {
  # we use the network configuration module for getting
  # all interfaces

  if (! scalar(@act)) {
    &foreign_check('net') || &error($text{'lib_err_netmod'});
    &foreign_require('net', 'net-lib.pl');
    @act = &foreign_call('net', 'active_interfaces');
    @act = sort { "$a->{'name'}:$a->{'virtual'}" cmp
                  "$b->{'name'}:$b->{'virtual'}" } @act;
    @act = grep($_->{'fullname'} !~ /ipsec/, @act);
  }
 
  my $a;
  foreach $a (@act) {
   $rv.="<OPTION VALUE=\"$a->{'fullname'}\"";
   $rv.=($a->{'fullname'} eq $sel) ? " SELECTED" : "";
   $rv.=">$a->{'fullname'}\n";
  }
 } else {
  # we parse the interfaces from the entered list
  my $a=$config{'netifaces'};
  $a=~tr/\s+//;
  my @act=split(/,/, $a);
  foreach $a (@act) {
   $rv.="<OPTION VALUE=\"$a\"";
   $rv.=($a eq $sel) ? " SELECTED" : "";
   $rv.=">$a\n";
  }
 }

 $rv.="</SELECT>\n";

return $rv;
}



# get_section(\parsed_config, section_type, section_name)
#
# Returns the parsed config for the section that matches the
# given type and name from parsed_config and undefined if no
# matching section was found.
# $_[0] == \@pc
# $_[1] == section_type
# $_[2] == section_name

sub get_section {
  my $rv=undef;
  foreach (@{$_[0]}) {
    if (($_->{'sectiontype'} eq $_[1]) && ($_->{'name'} eq $_[2])) {
      $rv=$_;
      last;
    }
  }
return $rv;
}



# section_append(\parsed_config, parsed_section, file_handle, line, [line [line [...]]]);
#
# Append the given line to the section that matches the given type and name.
# Give the parsed config as an reference to the array you get from
# parse_config and the file_handle from read_file_lines.
# Returns @parsed_config if caller wants array otherwise $section.

sub section_append {
  my $pc=shift;
  my $section=shift;
  my $file=shift;
  splice(@{$file}, $section->{'end__line'}+1, 0, @_);

  print "APPEND: $section->{'end__line'} ($section->{'name'})<BR>\n" if $_DEBUG;

  # Re-Parse config otherwise we will get   BadBugs (TM)
  @{$pc}=&parse_config();
  $section = &get_section(\@pc, $section->{'sectiontype'}, $section->{'name'});

return wantarray ? @{$pc} : $section;
}


# section_delete(\parsed_config, parsed_section, file_handle, key)
#
# Delete one or more values (defined by their keys) from a section.
# Returns @parsed_config if caller wants array otherwise $section.

sub section_delete {
  my $pc=shift;
  my $section=shift;
  my $file=shift;
  my $optname=shift;

  splice(@{$file}, $section->{"${optname}__line"}, 1);

  # Re-Parse config otherwise we will get   BadBugs (TM)
  @{$pc}=&parse_config();
  $section = &get_section(\@pc, $section->{'sectiontype'}, $section->{'name'});

return wantarray ? @{$pc} : $section;
}



# section_save(\pc, parsed_section, file_handle, option_name, default, value)
#
# Save an option to a section. Give the default value and the
# new value of the option named option_name.
# Returns @parsed_config if caller wants array otherwise $section.

sub section_save {

  # To make it easier to read:
  my $pc=shift;
  my $section=shift;
  my $file=shift;
  my $optname=shift;
  my $defval=shift;
  my $value=shift;
  my $newline="\t$optname=$value";
  my $rv=undef;

  if ($value ne $defval) {
    # Not the default so save to file

    if (defined($section->{$optname})) {
      # already defined so overwrite
      $file->[$section->{"${optname}__line"}] = $newline;

      # Re-Parse config otherwise we will get   BadBugs (TM)
      @{$pc}=&parse_config();
      $section = &get_section(\@pc, $section->{'sectiontype'}, $section->{'name'});

    } else {
      # Not yet defined, append to config setup section
      &section_append($pc, $section, $file, $newline);
    }

  } else {
    # It is the default, is it defined?
    if (defined($section->{$optname})) {
      # It is, so delete this entry
      &section_delete($pc, $section, $file, $optname);
    } # else not defined and default, have a nice day
  }

return wantarray ? @{$pc} : $section;
}



1;
### END of freeswan-lib.pl ###.
