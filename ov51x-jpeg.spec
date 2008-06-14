#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	Linux OVCam Drivers
Summary(pl.UTF-8):	Linuksowe sterowniki do kamer OVCam
Name:		ov51x-jpeg
Version:	1.5.7
Release:	%{_rel}
License:	GPL
Group:		Applications/Multimedia
Source0: http://www.rastageeks.org/downloads/ov51x-jpeg/ov51x-jpeg-1.5.7.tar.gz
# Source0-md5:	7de1f426a48bdb55218913e2d713f813
URL:		http://www.rastageeks.org/ov51x-jpeg/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_module_suffix	experimental
%define	_module_dir	kernel/drivers/media/video

%description
Linux OVCam Drivers.

%description -l pl.UTF-8
Linuksowe sterowniki do kamer OVCam.

%package -n kernel%{_alt_kernel}-video-%{name}
Summary:	Linux driver for OVCam webcams
Summary(pl.UTF-8):	Sterownik dla Linuksa do kamer internetowych OVCam
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
%endif

%description -n kernel%{_alt_kernel}-video-%{name}
This is driver for OVCam webcams for Linux.

%description -n kernel%{_alt_kernel}-video-%{name} -l pl.UTF-8
Sterownik dla Linuksa do kamer internetowych OVCam.

%prep
%setup -q
#sed -i -e '/#include <linux.videodev.h>/a #include <media/v4l2-dev.h>' \
#	*.[hc]
#sed -e '/EXTRA_CFLAGS/s/$/ -DHAVE_V4L2 -DCONFIG_VIDEO_PROC_FS/' -i Makefile

%build
%if %{with kernel}
%build_kernel_modules -m ov51x-jpeg
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m ov51x-jpeg -d %{_module_dir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/%{_module_dir}/*.ko*
#%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{name}.conf
%endif
