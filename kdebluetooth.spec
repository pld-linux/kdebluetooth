# TODO:
# - make it kdeextragears, not kdebluetooth-only
# - Killing gtk+ & xmms-libs deps?
%define		_beta	beta8
Summary:	KDE Bluetooth framework
Summary(pl.UTF-8):	Podstawowe środowisko KDE Bluetooth
Name:		kdebluetooth
Version:	1.0
Release:	0.%{_beta}.6
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/kde-bluetooth/%{name}-%{version}_%{_beta}.tar.bz2
# Source0-md5:	0b6aebf7d236894fc442d74425b13386
Source1:	kde-settings-network-bluetooth.menu
Source2:	network-bluetooth.menu
Patch0:		kde-common-PLD.patch
Patch1:		%{name}-dun_and_fax_handler-desktopfiles.patch
Patch2:		%{name}-nolibsdp.patch
Patch3:		kde-ac260-lt.patch
Patch4:		kde-am.patch
Patch5:		%{name}-gcc.patch
Patch6:		%{name}-debian.patch
URL:		http://bluetooth.kmobiletools.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6.1
BuildRequires:	bluez-libs-devel >= 2.6-2
BuildRequires:	dbus-qt-devel
BuildRequires:	gettext-devel
BuildRequires:	kdelibs-devel
BuildRequires:	kdepim-devel
BuildRequires:	libmad-devel
BuildRequires:	libvorbis-devel
BuildRequires:	lockdev-devel
BuildRequires:	obexftp-devel
BuildRequires:	openobex-devel >= 1.3-2
BuildRequires:	pkgconfig
BuildRequires:	qt-devel >= 6:3.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
BuildRequires:	xmms-devel
BuildRequires:	xorg-lib-libXrender-devel
Requires:	bluez-utils >= 3.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The KDE Bluetooth Framework is a set of tools built on top of Linux'
Bluetooth stack BlueZ. Its goal is to provide easy access to the most
common Bluetooth profiles and to make data exchange with Bluetooth
enabled phones and PDAs as straightforward as possible

%description -l pl.UTF-8
Projekt KDE Bluetooth jest zestawem narzędzi zbudowanych na górnej
warstwie stosu Bluetooth BlueZ. Jego celem jest dostarczenie łatwego
dostępu do większości profili Bluetooth oraz wymiany danych z
telefonami komórkowymi z Bluetooth oraz PDA tak bezpośrednio jak to
jest możliwe.

%package devel
Summary:	Header files for kdebluetooth libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek kdebluetooth
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bluez-libs-devel
Requires:	kdelibs-devel
# when no baudboy.h interface
Requires:	lockdev-devel

%description devel
Header files for kdebluetooth libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek kdebluetooth.

%prep
%setup -q -n %{name}-%{version}_%{_beta}
%patch0 -p1
#%patch1 -p1
#%patch2 -p1
%patch3 -p1
#%patch4 -p1
%patch5 -p0
%patch6 -p1

%build
cp %{_datadir}/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs

%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	%{!?debug:--disable-rpath} \
	--with-qt-libraries=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications-merged
install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications-merged

cp $RPM_BUILD_ROOT%{_datadir}/desktop-directories/{kde-settings-,}network-bluetooth.directory

mv $RPM_BUILD_ROOT%{_datadir}/applnk/Utilities/dunhandler.desktop \
	$RPM_BUILD_ROOT%{_desktopdir}/kde
mv $RPM_BUILD_ROOT%{_datadir}/applnk/Utilities/faxhandler.desktop \
	$RPM_BUILD_ROOT%{_desktopdir}/kde

for f in $RPM_BUILD_ROOT%{_desktopdir}/kde/kcm_*.desktop; do
	sed -i 's/Categories=Qt;KDE;X-KDE-settings-network/&-bluetooth/' $f
done

for f in $RPM_BUILD_ROOT%{_desktopdir}/kde/kb*.desktop; do
	sed -i 's/Categories=.*/Categories=Qt;KDE;X-bluetooth;/' $f
done

sed -i 's/Categories=Qt;KDE;X-bluetooth;/&TrayIcon;/' \
	$RPM_BUILD_ROOT%{_desktopdir}/kde/kbluetooth.desktop

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%{_sysconfdir}/xdg/menus/applications-merged/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_libdir}/kde3/kcm_*.la
%attr(755,root,root) %{_libdir}/kde3/kcm_*.so
%{_libdir}/kde3/kio_*.la
%attr(755,root,root) %{_libdir}/kde3/kio_*.so
%dir %{_libdir}/kdebluetooth
%dir %{_libdir}/kdebluetooth/servers
%attr(755,root,root) %{_libdir}/kdebluetooth/servers/kbtobexsrv
%dir %{_datadir}/apps/kdebluetooth
%dir %{_datadir}/apps/kdebluetooth/dunhandler
%attr(755,root,root) %{_datadir}/apps/kdebluetooth/dunhandler/dunhandler
%dir %{_datadir}/apps/kdebluetooth/faxhandler
%attr(755,root,root) %{_datadir}/apps/kdebluetooth/faxhandler/faxhandler
%attr(755,root,root) %{_datadir}/apps/kdebluetooth/faxhandler/kbtfax
%{_datadir}/apps/kdebluetooth/eventsrc
%dir %{_datadir}/apps/kbtobexclient
%{_datadir}/apps/kbtobexclient/kbtobexclientui.rc
%{_datadir}/apps/konqueror/servicemenus/kbtobexclient_sendfile.desktop
%{_datadir}/apps/konqsidebartng/virtual_folders/services/*.desktop
%{_datadir}/applnk/.hidden/kioobex_start.desktop
%{_datadir}/autostart/kbluetooth.autostart.desktop
%{_datadir}/desktop-directories/*
%{_datadir}/mimelnk/bluetooth
%{_datadir}/services/*
%{_datadir}/servicetypes/*
%{_desktopdir}/kde/*.desktop
%{_iconsdir}/[!l]*/*/*/*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%dir %{_includedir}/libkbluetooth
%{_includedir}/libkbluetooth/*.h
#%{_includedir}/libkbluetooth/*.cpp
%dir %{_includedir}/qobex
%{_includedir}/qobex/*.h
