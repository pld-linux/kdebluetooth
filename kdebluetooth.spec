#
# TODO:
# * applnk->vfolders
# * make it kdeextragears, not kdebluetooth-only 
# * breqs
# * fix files

%define		ver	3.3.2
Summary:	KDE Bluetooth framework
Summary(pl):	Podstawowe ¶rodowisko KDE Bluetooth
Name:		kdebluetooth
Version:	3.3.2
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	kdeextragear-3-%{ver}.tar.bz2	
# Source0-md5:	21c83484505cdeec5d3a55b62f0ac451
Patch0:         kdebluetooth_qttylock.cpp_dirtybuild.patch
URL:		http://kde-bluetooth.sourceforge.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6.1
BuildRequires:	bluez-libs-devel >= 2.6-2
BuildRequires:	gettext-devel
BuildRequires:	libmad-devel
BuildRequires:	libvorbis-devel
BuildRequires:	openobex-devel >= 1.0.0
BuildRequires:	qt-devel >= 3.1
BuildRequires:	xrender-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The long term goal of the KDE Bluetooth Framework is to provide tools
for all of the most common Bluetooth profiles.

%description -l pl
D³ugoterminowym celem projektu KDE Bluetooth Framework jest
dostarczenie narzêdzi do wszystkich najbardziej popularnych profili
Bluetooth. 

%package devel
Summary:	Header files for kdebluetooth libraries
Summary(pl):	Pliki nag³ówkowe bibliotek kdebluetooth
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kdelibs-devel

%description devel
Header files for kdebluetooth libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek kdebluetooth.

%prep
%setup -q -n kdeextragear-3-%{ver}
%patch0	-p1

%build
%{__make} -f Makefile.cvs
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	--disable-rpath \
	--with-qt-libraries=%{_libdir} \
	%{!?with_setup:--with-k3bsetup=no}
cd kdebluetooth	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd kdebluetooth
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	appsdir=%{_desktopdir}/kde \
	k3bsetup2dir=%{_desktopdir}/kde \
	kde_htmldir=%{_kdedocdir}
	

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files 
%defattr(644,root,root,755)
%doc README 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/kde3/kcm_*.so
%{_libdir}/kde3/kcm_*.la
%attr(755,root,root) %{_libdir}/kde3/kio_*.so
%{_libdir}/kde3/kio_*.la
%dir %{_libdir}/kdebluetooth
%attr(755,root,root) %{_libdir}/kdebluetooth/*
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/apps/kdebluetooth
%{_datadir}/applnk/.hidden/*.desktop
%{_desktopdir}/kde/*/*/*/*.desktop
%{_desktopdir}/kde/*/*/*.desktop
%{_desktopdir}/kde/*/*.desktop
%{_desktopdir}/kde/*.desktop
%{_datadir}/servicetypes/*
%{_datadir}/services/*
%{_datadir}/sounds/*
%{_iconsdir}/*/*/*/*.png
%{_datadir}/mimelnk/bluetooth
# XXX: dup (apps/kdebluetooth/*)
%{_datadir}/apps/*/*
%{_datadir}/config/*
%{_datadir}/desktop-directories/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqobex.so
%{_libdir}/libqobex.la
%{_includedir}/qobex
