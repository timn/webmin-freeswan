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

#    Created  : 28.12.2000


require "./freeswan-lib.pl";
@pc=&parse_config();
my $section=&get_section(\@pc, 'conn', $in{'conn'});
&error(&text('sconn_nof', $in{'conn'})) if (! defined($section) && ! defined($in{'name'}));

$cf = &read_file_lines($ipsec_conf);

if (defined($in{'name'})) {
  # New connection

  &error($text{'sconn_invname'}) if ($in{'name'} !~ /^[a-zA-Z][a-zA-Z0-9\._\-]*/);

  push(@{$cf}, "", "conn $in{'name'}");
  push(@$cf, "\ttype=$in{'type'}") if ($in{'type'} ne 'tunnel');
  push(@$cf, "\tauto=$in{'auto'}") if ($in{'auto'} ne 'ignore');
  push(@$cf, "\tcompress=$in{'compress'}") if ($in{'compress'} ne 'no');

  foreach $side (left, right) {
    push(@$cf, "\t$side=$in{$side}") if ($in{$side});
    push(@$cf, "\t${side}subnet=".$in{"sub$side"}) if ($in{"sub$side"});
    push(@$cf, "\t${side}nexthop=".$in{"gate$side"}) if ($in{"gate$side"});
    push(@$cf, "\t${side}updown=".$in{"updown$side"}) if ($in{"updown$side"});
    push(@$cf, "\t${side}firewall=".$in{"fw$side"}) if ($in{"fw$side"} && ($in{"fw$side"} ne 'no'));
  }

} elsif (defined($in{'delete'})) {
  # Delete a connection

  my $l=($section->{'end__line'} - $section->{'start__line'});
  $l++;     # Difference is one too less because we want also to delete start and
            # end line. Example: start__line=6, end__line=24, diff: 18, but we want
            # to delete 19 lines because we also include the start line. Got it?

  &error("Start: $section->{'start__line'} End: $section->{'end__line'} Length: $l") if $_DEBUG;

  splice(@{$cf}, $section->{'start__line'}, $l);

} else {
  # save a connection

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
}


&flush_file_lines();
if (defined($in{'name'})) {
  &redirect("edit_conn.cgi?conn=".&urlize($in{'name'}));
} elsif (defined($in{'delete'})) {
  &redirect();
} else {
  &redirect("edit_conn.cgi?conn=".&urlize($in{'conn'}));
}

### END of save_conn.cgi ###.
