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

#    Created  : 27.12.2000


require "./freeswan-lib.pl";
@pc=&parse_config();
my $section=&get_section(\@pc, 'config', 'setup');

$cf = &read_file_lines($ipsec_conf);


# We save the syslog settings
&section_save(\@pc, $section, $cf, 'syslog', "daemon.err", "$in{'syslfac'}.$in{'syslpri'}");

# We save the core dump settings
if ($in{'core'}) {
  &error($text{'sdebug_nocoredir'}) if (! $in{'coredir'});
  &section_save(\@pc, $section, $cf, 'dumpdir', "", $in{'coredir'});
} else {
  # we do not want core dumps
  &section_save(\@pc, $section, $cf, 'dumpdir', '', '');
}


# We save KLIPS debug settings
if ($in{'klipsmode'} == 1) {
  # All
  &section_save(\@pc, $section, $cf, 'klipsdebug', 'none', 'all');
} elsif ($in{'klipsmode'} == 2) {
  # None
  &section_save(\@pc, $section, $cf, 'klipsdebug', '', 'none');
} elsif ($in{'klipsmode'} == 3) {
  # Selected
  my @opts=split(/\0/, $in{'klipsdebug'});
  &error($text{'sdebug_klipsdebug'}) if (! scalar(@opts));
  my $newline='"'.join(' ', @opts).'"';
  &section_save(\@pc, $section, $cf, 'klipsdebug', 'none', $newline);
} else {
  &error($text{'sdebug_invcall'}, " (Code 1)");
}


# We save Pluto debug settings
if ($in{'plutomode'} == 1) {
  # All
  &section_save(\@pc, $section, $cf, 'plutodebug', 'none', 'all');
} elsif ($in{'plutomode'} == 2) {
  # None
  &section_save(\@pc, $section, $cf, 'plutodebug', '', 'none');
} elsif ($in{'plutomode'} == 3) {
  # Selected
  my @opts=split(/\0/, $in{'plutodebug'});
  &error($text{'sdebug_plutodebug'}) if (! scalar(@opts));
  my $newline='"'.join(' ', @opts).'"';
  &section_save(\@pc, $section, $cf, 'plutodebug', 'none', $newline);
} else {
  &error($text{'sdebug_invcall'}, " (Code 2)");
}



&flush_file_lines();
&redirect("edit_debug.cgi");

### END of save_debug.cgi ###.
