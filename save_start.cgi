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
my $section=&get_section(\@pc, 'config', 'setup');

$cf = &read_file_lines($ipsec_conf);



# Conns to load

if ($in{'loadmode'} == 1) {
  # None
  &section_save(\@pc, $section, $cf, 'plutoload', '', '');

} elsif ($in{'loadmode'} == 2) {
  # As defined for connections, use %search token
  &section_save(\@pc, $section, $cf, 'plutoload', '', '%search');

} elsif ($in{'loadmode'} == 3) {
  # As defined in list

  my @opts=split(/\0/, $in{'load'});
  &error($text{'sstart_noload'}) if (! scalar(@opts));
  my $newline='"'.join(' ', @opts).'"';

  &section_save(\@pc, $section, $cf, 'plutoload', '', $newline);

}


# Conns to start

if ($in{'startmode'} == 1) {
  # None
  &section_save(\@pc, $section, $cf, 'plutostart', '', '');

} elsif ($in{'startmode'} == 2) {
  # As defined for connections, use %search token
  &section_save(\@pc, $section, $cf, 'plutostart', '', '%search');

} elsif ($in{'startmode'} == 3) {
  # As defined in list

  my @opts=split(/\0/, $in{'start'});
  &error($text{'sstart_nostart'}) if (! scalar(@opts));
  my $newline='"'.join(' ', @opts).'"';

  &section_save(\@pc, $section, $cf, 'plutostart', '', $newline);

}



&flush_file_lines();
&redirect("edit_start.cgi");

### END of save_start.cgi ###.
