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
my $config=&get_section(\@pc, 'config', 'setup');


$cf = &read_file_lines($ipsec_conf);

if ($in{'defaultroute'}) {
  # We map ipsec0 to the defaultroute interface, that's easy ;)
  
  $cf->[$config->{"interfaces__line"}] = "\tinterfaces=\%defaultroute";

} else {
  # Interfaces are mapped individually

  @ipsecifcs=&get_ipsecifcs();
  @ifdef=();

  foreach $if (@ipsecifcs) {
    push(@ifdef, "$if=".$in{"realifc$if"});
  }
  
  if (! scalar(@ifdef)) {
    &error($text{'sifcs_nodef'});
  }

  $cf->[$config->{"interfaces__line"}] = "\tinterfaces=\"" . join(' ', @ifdef) . "\"";

}

&flush_file_lines();

&redirect("edit_ifcs.cgi");

### END of save_ifcs.cgi ###.
