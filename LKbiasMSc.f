C-----------------------------------------------------------------------
C
      program LKbias
C

      implicit double precision (a-h,o-z)

C     ---   Declaration of variables   ---

c      real ran  
c      character*4 ngc
c      character*72 fili
c      double precision lg


C     ---   Parametri   ---

c      parameter (nstar=500000)  ! number of objects
c      parameter (exp=2.0e0)     ! exponent of distance distribution
c      parameter (sigma=5.0d-5)  ! parallax error (in arscsec)
c      parameter (sigmam=0.2d0)  ! magnitude spread 
       
C     ---   Commons   ---

      common /reed/ iseed1,iseed2
 
      open(unit=2, file='LK.dat')  ! output file

      write(*,*) 'Output file LK.dat'

      write(*,*) '-----------------------------------------------'
      write(*,*) 'Select number of stars (1-500000)'
      read(*,*) nstar
      write(*,*) 'Select space distribution (exponent n of R^n' 
      write(*,*) 'distribution with R=distance between 1 pc and 8 Kpc)'
      write(*,*) 'n=2 --> constant spatial density of stars' 
      write(*,*) 'n=1 --> spatial density of stars decreasing as R^(-1)' 
      write(*,*) 'n=0 --> spatial density of stars decreasing as R^(-2)' 
      read(*,*) exp    
      write(*,*) 'Select type parallax error'
      write(*,*) 'GAIA-like error law =0 - Constant value=1'
      read(*,*)  indicepi
      if(indicepi.gt.0) then
      write(*,*) 'Select constant parallax error (arcsec)'
      read(*,*) sigma
      end if
      write(*,*) 'Select true mean absolute magnitude stars (mag)'
      read (*,*) zmvnp
      write(*,*) 'Select distribution true magnitudes'
      write(*,*) 'Gaussian=0 - Uniform=1'
      read(*,*) indice
      write(*,*) 'Select 1sigma true dispersion of the star' 
      write(*,*) 'absolute magnitude' 
      read(*,*) sigmam
      write(*,*) 'Select 1sigma photometric error (mag)' 
      write(*,*) 'on the measured apparent magnitude'
      read (*,*) photerr
      write(*,*) 'Do you want to include an apparent magnitude limit?'
      write(*,*) 'No=0  - Yes=1'
      read(*,*) indmaglim
      if(indmaglim.gt.0) then
      write(*,*) 'Select apparent magnitude limit (mag)' 
      read(*,*) zmaglim
      write(2,*) '----------------------------------------------'
      write(2,*) 'Apparent magnitude limit=', zmaglim
      end if
      write(*,*) '-----------------------------------------------'


       write(2,*) '-------------------------------------------------'
       write(2,*) 'Results simulation'       
       write(2,*) '(1) true parallax (arcsec)'
       write(2,*) '(2) true distance (pc)'
       write(2,*) '(3) apparent magnitude'
       write(2,*) '(4) observed parallax (arcsec)'
       write(2,*) '(5) parallax error (arcsec)'
       write(2,*) '(6) retrieved distance from observed parallax (pc)'
       write(2,*) '(7) true absolute magnitude'
       write(2,*) '(8) retrieved absolute magnitude'
       write(2,*) '(99.0 for negative derived distances)'
       write(2,*) '(9) photometric error (mag)'  
       write(2,*) '-------------------------------------------------'

C     ---   Initialization random extraction   ---
c      
       iseed1=860934
       iseed2=542039
c
       rdm=ran(iseed)
c
c
       zminf=0.001d0 ! Kpc  minimum distance
       zmsup=8.0d0    ! Kpc  maximum distance 
       if(exp.gt.0.0d0) then
       g=1.0d0/(1.0d0+exp)
       zmmin=g*(zminf**(1.0d0+exp))
       zmmax=g*(zmsup**(1.0d0+exp))
       zminc=zmmax-zmmin
       end if
c        


c       zmv=0.6d0   ! 'real' absolute magnitude of objects
c      if (indice.lt.0.9) then 
c      zmv=zmv+sigmam*gasdev(iseed) ! 'real' absolute magnitude with Gaussian distribution
c      else 
c      range=2.d0*dsqrt(3.d0)*sigmam
c     zmv=(zmv-dsqrt(3.d0)*sigmam)+ran(seed)*range ! 'real' absolute magnitude with uniform distribution
c     end if
c
       do 1 i=1,nstar

      if (indice.lt.0.9) then 
      zmv=zmvnp+sigmam*gasdev(iseed) ! 'real' absolute magnitude with Gaussian distribution
      else 
      range=2.d0*dsqrt(3.d0)*sigmam
      zmv=(zmvnp-(dsqrt(3.d0)*sigmam))+ran(iseed)*range ! 'real' absolute magnitude with uniform distribution
      end if


       if(exp.gt.0.0d0) then
       put=zminc*ran(iseed)+zmmin
       dist=(put/g)**g
       end if
       if(exp.eq.0.0d0) then
       dist=(zmsup-zminf)*ran(iseed)+zminf
       end if

       distpc=dist*1.0d3   ! real distance synthetic star (pc)
c       write(*,*) distpc
c      
       px=1.d0/(distpc)   ! real parallax synthetic star
c       write(*,*) px

       zmapp=zmv+5.d0*dlog10(distpc/10.0d0)   ! apparent magnitude synthetic stars

       if(indmaglim.gt.0) then
       if(zmapp.ge.zmaglim) goto 1    ! effect of magnitude limit
       end if


       if(indicepi.lt.1) then
       zfact=10.d0**(0.4d0*(zmapp-15.00d0))
       sigma1=(10.d0**(-6.d0))*
     # dsqrt(-1.631d0+680.766d0*zfact+32.732d0*zfact*zfact) ! GAIA-like parallax error (arcsec)
       sigma=dmax1(sigma1, 5.d-6)    
       end if

       pxobs=px+sigma*gasdev(iseed)  ! observed parallax with Gaussian error sigma
       
c       write(*,*) pxobs

       distpc2=1.d0/pxobs  ! derived distance

c       write(*,*) distpc2
       
       if(distpc2.gt.0.0d0) then
       zmvmeas=zmapp-(5.d0*dlog10(distpc2/10.0d0))
     #+photerr*gasdev(iseed) ! derived absolute magnitude + phot. error
       else       
       zmvmeas=99.d0   ! neglect negative distances
       end if

       write(2,100) px, distpc, zmapp, pxobs, sigma, 
     #distpc2, zmv, zmvmeas, photerr  ! write results

c       write(2,*) px, distpc

 1     continue

 100   format(1e12.4, f9.1, f8.3, 2e12.4, f15.1, 3f9.3)

       close(2)

       write(*,*) 'Written results in LK.dat'

       stop 

       end


      function ran(dummy)
C=======================================================================
C
C    This is an adapted version of subroutine RANECU written by
C    F. James (Comput. Phys. Commun. (1990) 60, 329-344), which 
C    has been modified to give a single random number at each call.
C    The seeds iseed1 and iseed2 must be initialized in the main 
C    program and transferred through the named common block /REED/.
C
C=======================================================================
	
      implicit double precision (a-h,o-z)
      implicit integer*4 (i)

C     ---   Declaracion de variables   ---

	real ran

C     ---   Parametros   ---

      parameter (uscale=1.0d0/2.0d0**31)

C     ---   Commons   ---

      common /reed/ iseed1,iseed2
 
C     ---   Calculo del numero aleatorio   ---

      i1=iseed1/53668
      iseed1=40014*(iseed1-i1*53668)-i1*12211

	 if (iseed1 .lt. 0) then
	 iseed2=iseed1+2147483563
	 else
	 continue
	 end if
 
      i2=iseed2/52774
      iseed2=40692*(iseed2-i2*52774)-i2*3791

	 if (iseed2 .lt. 0) then
	 iseed2=iseed2+2147483399
	 else
	 continue
	 end if
 
      iz=iseed1-iseed2

	 if (iz .lt. 1) then
	 iz=iz+2147483562
	 else
	 continue
	 end if

      ran=iz*uscale
 
      return

C***********************************************************************

      end 


      function gasdev(iseed)
C=======================================================================
C
C     Returns a normally distributed deviate with zero mean and unit
C     variance.
C
C=======================================================================
      implicit double precision (a-h,o-z)

C     ---   Variable declaration   ---

      real ran

C     ---   Use static memory   ---

      save

C     ---   Data   ---

      data iset /0/

C     ---   We don't have an extra deviate handy, so ...   ---

	 if (iset .eq. 0) then

    1    continue

C     ---   pick two uniform numbers in the square (-1,+1)

	 v1=2.0d0*ran(iseed)-1.0d0
	 v2=2.0d0*ran(iseed)-1.0d0

C     ---   See if they are in the unit circle   ---

	 r=v1*v1+v2*v2

C     ---   and if they are not, try again   ---

	    if (r .ge. 1.0d0 .or. r .eq. 0.0d0) then
	    go to 1
	    else
	    continue
	    end if

C     ---  Make Box-Muller transformation to get 2 normal deviates   ---

	 fac=dsqrt(-2.0d0*dlog(r)/r)

C     ---   return one and save the other for the next time   ---

	 gset=v1*fac
	 gasdev=v2*fac
	 iset=1

	 else

C     ---   We have an extra deviate so return it and unset flag   ---

	 gasdev=gset
	 iset=0

	 end if

      return

C***********************************************************************

      end

