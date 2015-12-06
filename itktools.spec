%global commit 5a2167305a5c343d1d1c0eee9bfc4738571396b9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           itktools
Version:        0.3.1
Release:        0.2.git%{shortcommit}%{?dist}
Summary:        Practical command line tools based on the ITK

License:        ASL 2.0
URL:            https://github.com/ITKTools/ITKTools
Source0:        https://github.com/ITKTools/ITKTools/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  InsightToolkit-devel
BuildRequires:  vxl-devel
BuildRequires:  gdcm-devel /usr/bin/gdcmdump
BuildRequires:  fftw-devel
Requires:       python3

%description
Practical command line tools based on the ITK, intended for image processing.
These tools are designed to take one or more input image(s) from the command
line, perform a single operation, and produce an output image. For example
smoothing of an image can be done with the tool pxgaussianimagefilter.

%prep
%autosetup -n ITKTools-%{commit}

mkdir -p build/

%build
pushd build/
  export ITK_DIR=%{_libdir}/cmake/InsightToolkit
  %cmake ../src/ -DUSE_FFTIMAGE=ON -DITKTOOLS_4D_SUPPORT=ON -DITKTOOLS_BUILD_TESTING=ON
  %make_build
popd

%install
pushd build/
  %make_install
popd

# add shebang for python stuff
sed -i -e '1i#!/usr/bin/python3' %{buildroot}%{_bindir}/*.py

%check
pushd build/
  # https://github.com/ITKTools/ITKTools/issues/64
  %ifarch %{ix86}
    %global skip_tests meanstdimage_SAMSTD_COMPARE
  %endif
  ctest -VV %{?skip_tests:-E %{skip_tests}}
popd

%files
%license LICENSE
%doc README.md
%{_bindir}/px*

%changelog
* Sun Dec 06 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3.1-0.2.git5a21673
- Change name to itktools
- Skip tests

* Mon Nov 09 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3.1-0.1.git5a21673
- Initial package
