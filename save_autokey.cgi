#!/usr/bin/perl
#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module
#    Copyright (C) 1999-2000 by Tim Niemueller <tim@niemueller.de>
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

#    Created  : 28.12.2000


require "./freeswan-lib.pl";
@pc=&parse_config();
my $section=&get_section(\@pc, 'conn', $in{'conn'});
&error(&text('sconn_nof', $in{'conn'})) if (! defined($section));

$cf = &read_file_lines($ipsec_conf);

# Key Exchange Method
&section_save(\@pc, $section, $cf, 'keyexchange', 'ike', $in{'keyexchange'});

# Perfect Forward Secrecy?
&section_save(\@pc, $section, $cf, 'pfs', 'yes', $in{'perffor'});

# Authentication protocol
&section_save(\@pc, $section, $cf, 'auth', 'esp', $in{'auth'});

# Authentication method
&section_save(\@pc, $section, $cf, 'authby', 'secret', $in{'authby'});


foreach $side (left, right) {

  # ID
  if ($in{"${side}def"}) {
    &section_save(\@pc, $section, $cf, "${side}id", '', '');
  } else {
    &section_save(\@pc, $section, $cf, "${side}id", '', $in{"${side}id"});
  }

  # RSA key
  if ($in{"${side}rsamode"} == 1) {
    # None
    &section_save(\@pc, $section, $cf, "${side}rsasigkey", '', '');
  } elsif ($in{"${side}rsamode"} == 2) {
    # From DNS
    &section_save(\@pc, $section, $cf, "${side}rsasigkey", '', '%dns');
  } elsif ($in{"${side}rsamode"} == 3) {
    # User gave it
    &section_save(\@pc, $section, $cf, "${side}rsasigkey", '', $in{"${side}rsa"});
  } # not from right form, ignore, to lazy for error :-)

}


# Keylife
&section_save(\@pc, $section, $cf, 'keylife', '', $in{'keylife'});

# Re-Key Margin
&section_save(\@pc, $section, $cf, 'rekeymargin', '', $in{'rekeymargin'});

# Inc Margin factor
&section_save(\@pc, $section, $cf, 'rekeyfuzz', '', $in{'rekeyfuzz'});

# No. of Keying Tries
&section_save(\@pc, $section, $cf, 'keyingtries', '', $in{'keyingtries'});

# IKE Connection Lifetime
&section_save(\@pc, $section, $cf, 'ikelifetime', '', $in{'ikelifetime'});


&flush_file_lines();
&redirect("edit_autokey.cgi?conn=".&urlize($in{'conn'}));

### END of save_conn.cgi ###.
