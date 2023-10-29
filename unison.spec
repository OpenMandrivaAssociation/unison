%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%bcond_with doc
# FIXME: ocaml-lablgtk3-devel has not been packaged yet
%bcond_with gui


Summary:	File-synchronization tool for Unix and Windows
Name:		unison
Version:	2.53.3
Release:	1
License:	GPLv2+
Group:		File tools
Url:		http://www.cis.upenn.edu/~bcpierce/unison/
Source0:	https://github.com/bcpierce00/unison/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
#Source1:	unison.png
#Source2:	%{name}-%{version}-manual.pdf
Buildrequires:	ocaml
BuildRequires:	emacs-common
BuildRequires:	imagemagick
BuildRequires:	librsvg
%if %{with gui}
BuildRequires:	ocaml-lablgtk3-devel
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
%if %{with doc}
BuildRequires:	texlive
%endif

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
%license LICENSE
%doc NEWS.md README.md
%doc src/CONTRIB src/README src/ROADMAP.txt
%if %{with doc}
%doc doc/unison-manual.pdf
%endif
%{_bindir}/*
%if %{with gui}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.svg
%endif
%{_mandir}/man1/%{name}.1*

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%make_build \
	STATIC=false \
	DEBUGGING=true \
	THREADS=true \
%if %{with gui}
	UISTYLE=gtk3 \
%endif
	NATIVE=true \
	%{nil}

# docs
%if %{with doc}
%make_build docs
%endif

%install
# binary
install -m755 src/%{name} -D %{buildroot}%{_bindir}/%{name}

# manpage
install -Dm 0644 man/%{name}.1 -t %{buildroot}%{_mandir}/man1/

%if %{with gui}
# icons
install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
install -Dm 0644 icons/U.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" icons/U.svg \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -size 32x32 icons/U.svg %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# .desktop
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
%endif

