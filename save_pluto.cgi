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
my $section=&get_section(\@pc, 'config', 'setup');


$cf = &read_file_lines($ipsec_conf);


# Run Pluto?
&section_save(\@pc, $section, $cf, 'pluto', 'yes', $in{'run'});

# Wait for negotiation attempt?
&section_save(\@pc, $section, $cf, 'plutowait', 'yes', $in{'wait'});

# Load and start conns in background?
&section_save(\@pc, $section, $cf, 'plutobackgroundload', 'no', $in{'bg'});

# Pre Pluto Command
&section_save(\@pc, $section, $cf, 'prepluto', '', $in{'pre'});

# Post Pluto Command
&section_save(\@pc, $section, $cf, 'postpluto', '', $in{'post'});


&flush_file_lines();
&redirect("edit_pluto.cgi");

### END of save_pluto.cgi ###.
