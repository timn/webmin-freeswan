#!/usr/bin/perl
#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module
#    Copyright (C) 2000-2001 by Tim Niemueller <tim@niemueller.de>
#    http://www.niemueller.de/webmin/modules/freeswan/
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

#    Created  : 29.12.2000


require "./freeswan-lib.pl";
@pc=&parse_config();
my $section=&get_section(\@pc, 'conn', $in{'conn'});
&error(&text('sconn_nof', $in{'conn'})) if (! defined($section));

$cf = &read_file_lines($ipsec_conf);


# SPI
&section_save(\@pc, $section, $cf, 'spi', '', $in{'spi'});

# Base SPI
&section_save(\@pc, $section, $cf, 'spibase', '', $in{'spibase'});

# ESP Method
&section_save(\@pc, $section, $cf, 'esp', '', $in{'esp'});

# AH Method
&section_save(\@pc, $section, $cf, 'ah', '', $in{'ah'});



# ESP Enc Key
my $espenckey;                  # Just for the taste of it an "use strict"

if ($in{'useespenckey'} == 1) {
  # None/From ipsec.secrets
  $espenckey='';                # Not really needed but better to read

} elsif ($in{'useespenckey'} == 2) {
  # Automatic, we generate a key with 192 ranbits for 3DES

  &error($text{'smk_noespauth'}) if ($in{'esp'} !~ /3des/);

  $espenckey=`$ipsec_comm ranbits 192`;
  chomp $espenckey;

} elsif ($in{'useespenckey'} == 3) {
  $espenckey=$in{'espenckey'};
}
&section_save(\@pc, $section, $cf, 'espenckey', '', $espenckey);



# ESP Auth Key
my $espauthkey;                  # Just for the taste of it an "use strict"
my $bitcount=undef;

if ($in{'useespauthkey'} == 1) {
  # None/From ipsec.secrets
  $espauthkey='';                # Not really needed but better to read

} elsif ($in{'useespauthkey'} == 2) {
  # Automatic, we generate a key with 192 ranbits for 3DES

  &error($text{'smk_noespauth'}) if ($in{'esp'} !~ /(sha1|md5)/);

  if ($in{'esp'} =~ /md5/) {
    # MD5
    $bitcount=128;
  } elsif ($in{'esp'} =~ /sha1/) {
    # SHA1
    $bitcount=160;
  } # else no Authentication, no key needed

  $espauthkey=($bitcount) ? `$ipsec_comm ranbits $bitcount` : '';
  chomp $espauthkey;

} elsif ($in{'useespauthkey'} == 3) {
  $espauthkey=$in{'espauthkey'};
}
&section_save(\@pc, $section, $cf, 'espauthkey', '', $espauthkey);



# AH Auth Key
my $ahauthkey;                  # Just for the taste of it an "use strict"
my $bitcount=undef;

if ($in{'useahauthkey'} == 1) {
  # None/From ipsec.secrets
  $ahauthkey='';                # Not really needed but better to read

} elsif ($in{'useahauthkey'} == 2) {
  # Automatic, we generate a key with 192 ranbits for 3DES

  &error($text{'smk_noah'}) if (! $in{'ah'});

  if ($in{'ah'} =~ /md5/) {
    # MD5
    $bitcount=128;
  } elsif ($in{'ah'} =~ /sha1/) {
    # SHA1
    $bitcount=160;
  } # else no Authentication, no key needed

  $ahauthkey=($bitcount) ? `$ipsec_comm ranbits $bitcount` : '';;
  chomp $ahauthkey;

} elsif ($in{'useahauthkey'} == 3) {
  $ahauthkey=$in{'ahauthkey'};
}

&section_save(\@pc, $section, $cf, 'ahauthkey', '', $ahauthkey);



# AH Replay Window
&section_save(\@pc, $section, $cf, 'ahreplay_window', '0', $in{'ahrwin'});



foreach $side (left, right) {

  # $_ ESP SPI
  &section_save(\@pc, $section, $cf, "${side}espspi", '', $in{"${side}espspi"});

  # $_ AH SPI
  &section_save(\@pc, $section, $cf, "${side}ahspi", '', $in{"${side}ahspi"});



  # $_ ESP Enc Key
  my $espenckey=undef;

  if ($in{"use${side}espenckey"} == 1) {
    # None/From ipsec.secrets
    $espenckey='';                # Not really needed but better to read

  } elsif ($in{"use${side}espenckey"} == 2) {
    # Automatic, we generate a key with 192 ranbits for 3DES
    &error($text{'smk_noespauth'}) if ($in{'esp'} !~ /3des/);
    $espenckey=`$ipsec_comm ranbits 192`;
    chomp $espenckey;

  } elsif ($in{"use${side}espenckey"} == 3) {
    $espenckey=$in{"${side}espenckey"};
  }
  &section_save(\@pc, $section, $cf, "${side}espenckey", '', $espenckey);


  # ESP Auth Key
  my $espauthkey=undef;                  # Just for the taste of it an "use strict"
  my $bitcount=undef;

  if ($in{"use${side}espauthkey"} == 1) {
    # None/From ipsec.secrets
    $espauthkey='';                # Not really needed but better to read

  } elsif ($in{"use${side}espauthkey"} == 2) {
    # Automatic, we generate a key with 192 ranbits for 3DES

    &error($text{'smk_noespauth'}) if ($in{'esp'} !~ /(sha1|md5)/);

    if ($in{'esp'} =~ /md5/) {
      # MD5
      $bitcount=128;
    } elsif ($in{'esp'} =~ /sha1/) {
      # SHA1
      $bitcount=160;
    } # else no Authentication, no key needed

    $espauthkey=($bitcount) ? `$ipsec_comm ranbits $bitcount` : '';
    chomp $espauthkey;

  } elsif ($in{"use${side}espauthkey"} == 3) {
    $espauthkey=$in{"${side}espauthkey"};
  }
  &section_save(\@pc, $section, $cf, "${side}espauthkey", '', $espauthkey);



  # AH Auth Key
  my $ahauthkey=undef;                  # Just for the taste of it an "use strict"
  my $bitcount=undef;

  if ($in{"use${side}ahauthkey"} == 1) {
    # None/From ipsec.secrets
    $ahauthkey='';                # Not really needed but better to read

  } elsif ($in{"use${side}ahauthkey"} == 2) {
    # Automatic, we generate a key with 192 ranbits for 3DES

    &error($text{'smk_noah'}) if (! $in{'ah'});

    if ($in{'ah'} =~ /md5/) {
      # MD5
      $bitcount=128;
    } elsif ($in{'ah'} =~ /sha1/) {
      # SHA1
      $bitcount=160;
    } # else no Authentication, no key needed

    $ahauthkey=($bitcount) ? `$ipsec_comm ranbits $bitcount` : '';
    chomp $ahauthkey;

  } elsif ($in{"use${side}ahauthkey"} == 3) {
    $ahauthkey=$in{"${side}ahauthkey"};
  }
  &section_save(\@pc, $section, $cf, "${side}ahauthkey", '', $ahauthkey);

}



&flush_file_lines();
&redirect("edit_mankey.cgi?conn=".&urlize($in{'conn'}));

### END of save_mankey.cgi ###.
