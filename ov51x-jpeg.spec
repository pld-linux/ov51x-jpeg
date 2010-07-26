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
Version:	1.5.9
Release:	%{_rel}
License:	GPL
Group:		Applications/Multimedia
Source0:	http://www.rastageeks.org/downloads/ov51x-jpeg/%{name}-%{version}.tar.gz
# Source0-md5:	95041de8e908f1548df3d4e1f6ed2a94
# https://svn.pardus.org.tr/pardus/2009/devel/kernel/pae/drivers/module-pae-ov51x-jpeg/files/ov51x-jpeg-2.6.30.patch
Patch0:		%{name}-2.6.30.patch
# https://svn.pardus.org.tr/pardus/2009/devel/kernel/pae/drivers/module-pae-ov51x-jpeg/files/ov51x-jpeg-2.6.29.patch
Patch1:		%{name}-2.6.29.patch
# https://svn.pardus.org.tr/pardus/2009/devel/kernel/pae/drivers/module-pae-ov51x-jpeg/files/kernel_messages.patch
Patch2:		kernel_messages.patch
# https://svn.pardus.org.tr/pardus/2009/devel/kernel/pae/drivers/module-pae-ov51x-jpeg/files/v4lcompat_old_kernels_only.patch
Patch3:		v4lcompat_old_kernels_only.patch
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
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
