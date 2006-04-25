#
# TODO:
# * make it kdeextragears, not kdebluetooth-only
# * Killing gtk+ & xmms-libs deps?
Summary:	KDE Bluetooth framework
Summary(pl):	Podstawowe ¶rodowisko KDE Bluetooth
Name:		kdebluetooth
Version:	1.0
%define		_beta	beta1
Release:	0.%{_beta}.8
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/kde-bluetooth/%{name}-%{version}_%{_beta}.tar.bz2
# Source0-md5:	11244d5acf07a79e04a447ff2a3bccdf
Source1:	kde-settings-network-bluetooth.menu
Source2:	network-bluetooth.menu
Patch0:		%{name}-dun_and_fax_handler-desktopfiles.patch
Patch1:		%{name}-nolibsdp.patch
Patch2:		%{name}-debian.patch
URL:		http://kde-bluetooth.sourceforge.net/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6.1
BuildRequires:	bluez-libs-devel >= 2.6-2
BuildRequires:	gettext-devel
BuildRequires:	libmad-devel
BuildRequires:	libvorbis-devel
BuildRequires:	lockdev-devel
BuildRequires:	kdelibs-devel
BuildRequires:	kdepim-devel
BuildRequires:	openobex-devel >= 1.0.0
BuildRequires:	qt-devel >= 3.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:  sed >= 4.0
BuildRequires:	xmms-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The KDE Bluetooth Framework is a set of tools built on top of Linux'
Bluetooth stack BlueZ. Its goal is to provide easy access to the most
common Bluetooth profiles and to make data exchange with Bluetooth
enabled phones and PDAs as straightforward as possible

%description -l pl
Projekt KDE Bluetooth jest zestawem narzêdzi zbudowanych na górnej
warstwie stosu Bluetooth BlueZ. Jego celem jest dostarczenie ³atwego
dostêpu do wiêkszo¶ci profili Bluetooth oraz wymiany danych z
telefonami komórkowymi z Bluetooth oraz PDA tak bezpo¶rednio jak to
jest mo¿liwe.

%package devel
Summary:	Header files for kdebluetooth libraries
Summary(pl):	Pliki nag³ówkowe bibliotek kdebluetooth
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bluez-libs-devel
Requires:	kdelibs-devel
# when no baudboy.h interface
Requires:	lockdev-devel

%description devel
Header files for kdebluetooth libraries.

%description devel -l pl
Pliki nag³ówkowe bibliotek kdebluetooth.

%prep
%setup -q -n %{name}-%{version}_%{_beta}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp %{_datadir}/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs

%configure \
	--%{!?debug:dis}%{?debug:en}able-debug \
	%{!?debug:--disable-rpath} \
	--with-bluetooth-libraries=%{_libdir} \
	--with-qt-libraries=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

install -d $RPM_BUILD_ROOT/etc/xdg/menus/applications-merged
install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT/etc/xdg/menus/applications-merged

cp $RPM_BUILD_ROOT%{_datadir}/desktop-directories/{kde-settings-,}network-bluetooth.directory

mv $RPM_BUILD_ROOT%{_datadir}/applnk/Settings/Peripherals/obex.desktop \
	$RPM_BUILD_ROOT%{_desktopdir}/kde
echo "Categories=Qt;KDE;X-KDE-settings-peripherals;" \
	>> $RPM_BUILD_ROOT%{_desktopdir}/kde/obex.desktop	

for f in $RPM_BUILD_ROOT%{_desktopdir}/kde/kcm_*.desktop; do
	sed -i 's/Categories=Qt;KDE;X-KDE-settings-network/&-bluetooth/' $f
done

for f in $RPM_BUILD_ROOT%{_desktopdir}/kde/kb*.desktop; do
	sed -i 's/Categories=.*/Categories=Qt;KDE;X-bluetooth;/' $f
done

sed -i 's/Categories=Qt;KDE;X-bluetooth;/&TrayIcon;/' \
	$RPM_BUILD_ROOT%{_desktopdir}/kde/kbluetoothd.desktop

%find_lang %{name}    --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
/etc/xdg/menus/applications-merged/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/libqobex.so.*.*.*
%{_libdir}/libirmcsynckonnector.la
%attr(755,root,root) %{_libdir}/libirmcsynckonnector.so
%{_libdir}/kde3/kcm_*.la
%attr(755,root,root) %{_libdir}/kde3/kcm_*.so
%{_libdir}/kde3/kio_*.la
%attr(755,root,root) %{_libdir}/kde3/kio_*.so
%dir %{_libdir}/kdebluetooth
%attr(755,root,root) %{_libdir}/kdebluetooth/*
%{_datadir}/applnk/.hidden/*
%{_datadir}/apps/kbluetoothd
%{_datadir}/apps/kbtobexclient
%dir %{_datadir}/apps/kdebluetooth
%dir %{_datadir}/apps/kdebluetooth/dunhandler
%attr(755,root,root) %{_datadir}/apps/kdebluetooth/dunhandler/dunhandler
%dir %{_datadir}/apps/kdebluetooth/faxhandler
%attr(755,root,root) %{_datadir}/apps/kdebluetooth/faxhandler/faxhandler
%attr(755,root,root) %{_datadir}/apps/kdebluetooth/faxhandler/kbtfax
%{_datadir}/apps/kdebluetooth/job-templates
%{_datadir}/apps/konqsidebartng/virtual_folders/services/*.desktop
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/autostart/kbluetoothd.autostart.desktop
%{_datadir}/config/*
%{_datadir}/desktop-directories/*
%{_datadir}/mimelnk/bluetooth
%{_datadir}/services/*
%{_datadir}/servicetypes/*
%{_desktopdir}/kde/*.desktop
%{_iconsdir}/[!l]*/*/*/*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqobex.so
%{_libdir}/libqobex.la
%{_includedir}/qobex
