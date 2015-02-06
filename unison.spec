%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Summary:	File-synchronization tool for Unix and Windows
Name:		unison
Version:	2.40.102
Release:	2
License:	GPLv2+
Group:		File tools
Url:		http://www.cis.upenn.edu/~bcpierce/unison/
Source0:	%{name}-%{version}.tar.gz
Source1:	unison.png
Source2:	%{name}-%{version}-manual.pdf
Buildrequires:	ocaml
BuildRequires:	emacs-common
BuildRequires:	ocaml-lablgtk2-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
Requires:	openssh-clients
Requires:	x11-font-schumacher-misc
Requires:	rsync

%description
Unison is a file-synchronization tool for Unix and Windows. It allows
two replicas of a collection of files and directories to be stored on
different hosts (or different disks on the same host), modified
separately, and then brought up to date by propagating the changes in
each replica to the other. Unlike simple mirroring or backup
utilities, Unison can deal with updates to both replicas of a
distributed directory structure. Updates that do not conflict are
propagated automatically.  Conflicting updates are detected and
displayed. Unison can synchronize either locally (between volumes
mounted on the same computer) or remotely,between any pair of machines
connected to the internet, communicating over either a direct socket
link or tunneling over an rsh or an encrypted ssh connection. It is
careful with network bandwidth, and runs well over slow links such as
PPP connections. Unison is available for both Windows (95/98/NT/2K)
and Unix (Linux, Solaris). Moreover, Unison works across platforms,
allowing you to synchronize a Windows laptop with a Unix server, for
example.

%files
%doc NEWS RECENTNEWS TODO.txt README CONTRIB COPYING %{name}-%{version}-manual.pdf
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*

#----------------------------------------------------------------------------

%prep
%setup -q

%build
make THREADS=true UISTYLE=gtk2

%install
mv src/* ./
install -m755 %{name} -D %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -f %{SOURCE1} %{buildroot}%{_datadir}/pixmaps
cp -f %{SOURCE2} .

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=System;Utility;
EOF

