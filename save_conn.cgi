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


# Type
&section_save(\@pc, $section, $cf, 'type', 'tunnel', $in{'type'});

# Load/Start?
&section_save(\@pc, $section, $cf, 'auto', 'ignore', $in{'auto'});

# Compress?
&section_save(\@pc, $section, $cf, 'compress', 'no', $in{'compress'});

foreach $side (left, right) {

  # IP
  &section_save(\@pc, $section, $cf, $side, '', $in{$side});

  # Subnet
  &section_save(\@pc, $section, $cf, "${side}subnet", '', $in{"sub$side"});

  # Next Gateway
  &section_save(\@pc, $section, $cf, "${side}nexthop", '', $in{"gate$side"});

  # Up/Down Script
  &section_save(\@pc, $section, $cf, "${side}updown", '', $in{"updown$side"});

  # Punch Firewall Holes?
  &section_save(\@pc, $section, $cf, "${side}firewall", 'no', $in{"fw$side"});

}


&flush_file_lines();
&redirect("edit_conn.cgi?conn=".&urlize($in{'conn'}));

### END of save_conn.cgi ###.
