close all
clear all

xSize=9;
ySize=9;

%%Figure init
figure(1);
set(figure(1),'units','centimeters','position',[2 15 xSize ySize]);
xlabel('Mass fraction');ylabel('Surface Tension (mN/m)');
hold on;

figure(2);
set(figure(2),'units','centimeters','position',[13 15 xSize ySize]);
xlabel('Mass fraction (%)');ylabel('Density (kg/m^3)');
hold on;

figure(3);
set(figure(3),'units','centimeters','position',[24 15 xSize ySize]);
xlabel('Mass fraction (%)');ylabel('Refractive index')
hold on;

figure(33);
set(figure(33),'units','centimeters','position',[24 15 xSize ySize]);
xlabel('Concentration (mol/L)');ylabel('Refractive index')
hold on;

figure(4);
set(figure(4),'units','centimeters','position',[24 2 xSize ySize]);
xlabel('Mass fraction');ylabel('Osmotic coefficient');
hold on;

figure(5);
set(figure(5),'units','centimeters','position',[13 2 xSize ySize]);
xlabel('Mass fraction');ylabel('Humidity (%)'); 
hold on;

figure(6);
set(figure(6),'units','centimeters','position',[2 2 xSize ySize]);
xlabel('Mass fraction');ylabel('Mean activity coefficient of solute');
hold on;

%Constants
Mmna=58.44e-3; %molar mass (kg/mol)
Mmk=74.6e-3; %molar mass (kg/mol)
Mmli=42.4e-3; %molar mass (kg/mol)
Mmwa=18e-3; % molar mass(kg/mol)

%%
Th2o=647.226; %Critical temperature of water (K)
T=298; %Temperature (K)
teta=T/Th2o; %Reduced temperature
%Mass fraction of solute
cpli=(1:570)/1000;

%%%REDUCED PRESSURE OF LiCl%%% (Conde, IJTS 43, 2004, 367-382)
%Pli=psol/ph2o
%Coefficient
pi1=4.30;pi2=0.6;pi3=0.21;pi4=5.1;pi5=0.49;pi6=0.362;pi7=-4.75;pi8=-0.4;
pi9=0.03;pi0=0.28;
a=2-(1+(cpli/pi0).^pi1).^pi2;
b=(1+(cpli/pi3).^pi4).^pi5-1;

fx=a+b*teta;
pi25=1-(1+(cpli/pi6).^pi7).^pi8-pi9*exp(-(cpli-0.1).^2/0.005);

%Pressure
Pli=pi25.*fx*100;

molalityli=1./(Mmli*(1./cpli-1));
figure(5);
plot(cpli,Pli,'g');hold on;

%Osmotic coefficient of LiCl
phili3=-1000*log(Pli/100)./(molalityli*42.4);

%%%ACTIVITY OF SOLVENT FOR LiCl%%%
Mw=18;
awli=exp(-phili3.*molalityli.*Mmwa*2); %molality
mflii=1./(1+1./(molalityli*Mmli));
figure(4);
plot(mflii,phili3,'k');hold on;
figure(7)
plot(mflii,awli,'g');hold on;

%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SURFACE TENSION %%%%%%%%%%%%%%%%%%%%%%%%%%

%%%SURFACE TENSION OF LiCl%%% (Conde, IJTS 43, 2004, 367-382)
Th2o=643.847; %Critical temperature of water (K)
T=293; %Temperature (K)
teta=T/Th2o; %Reduced temperature

%Surface tension of water IAPWS
s0=235.8; %mN/m
b=-0.625;
mu=1.256;
geau=s0*(1+b*(1-teta))*(1-teta)^mu; 

%Coefficient from experimental data 
c1=2.757115;
c2=-12.011299;
c3=14.751818;
c4=2.443204;
c5=-3.147739;

cgli=(0:44)/100; %mass fraction solubility water at 20°C

%Surface tension 
gli= geau*(1+c1.*cgli+c2.*cgli.*teta+c3.*cgli.*teta^2+c4.*cgli.^2+c5.*cgli.^3); %mN/m

%%%SURFACE TENSION OF NaCl%%% (Dutcher, JPC, 2010, 114, 12216-12230) 

%Coefficient
aws=232.54;
bws=-0.245;
asw=-142.42;
bsw=0;
c1=191.16;
c2=-0.0747;

xs=(0:140)/1000; %mole fraction of salt
xw=1-xs; %mole fraction of water
T=273+15; %K
Fws=aws+bws*T;%T temperature (K)
Fsw=asw+bsw*T;
xs2=Mmna*xs*1./(Mmna*xs+Mmwa*xw); % mass fraction

%Surface tension of water
gw=235.8*((647.15-T)/647.15)^1.256*(1-0.625*((647.15-T)/647.15));
%Surface tension of molten salt
gs=c1+c2*T;
%Surface tension
gna=exp(xw.*log(gw+Fws.*xs)+xs.*log(gs+Fsw.*xw)); %mN/m

%%%SURFACE TENSION OF KCl%%% (Dutcher, JPC, 2010, 114, 12216-12230) 

%Coefficients
aws=-117.33;
bws=0.489;
asw=0;
bsw=0;
c1=177.61;
c2=-0.07519;

xs=(0:75)/1000; %mole fraction of salt, solubility in water at 20°C
xw=1-xs; %mole fraction of water
xs2k=Mmk*xs*1./(Mmk*xs+Mmwa*xw); % mass fraction

Fws=aws+bws*T;%T temperature (K)
Fsw=asw+bsw*T;

%Surface tension of water
gw=235.8*((647.15-T)/647.15)^1.256*(1-0.625*((647.15-T)/647.15));
%Surface tension of molten salt
gs=c1+c2*T;
%Surface tension, xw mole fraction of water, xs mole fraction of salt
gk=exp(xw.*log(gw+xs*Fws)+xs.*log(gs+xw*Fsw)) ; %(mN/m)

figure(1)
plot(cgli,gli,'g');hold on;
plot(xs2,gna,'b');hold on;
plot(xs2k,gk,'r');


%%

%%%%%%%%%%%%%%%%%%%%%%%%%%% DENSITY %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%DENSITY OF NaCl%%% (Simion, JAPT, 2015, 21, 41-52)
%Coefficient
b1=919.0202567;
b2=8.661163416;
b3=0.854264859;
b4=0.027175948;
b5=-0.00199299;
b6=-0.00585389;
T=298.15;
rhoeau=997;%kg/m^3
rhos=2.16e-3/(1e-6); %kg/m^3 (2.16g/cm^3)
crhona=(0:263)/1000*100; %mass fraction (%)
rhona=b1+b2*crhona+b3*T+b4*crhona.^2+b5*T^2+b6*T*crhona; %kg/m3
%Hargreaves, JPCA, 2010, 114,1806-1815
rhona2=((1-crhona/100)/rhoeau+crhona/(100*rhos)).^(-1);%kg/m^3

%%%DENSITY OF LiCl%%% (Conde, IJTS 43, 2004, 367-382)

%Coefficient
rho0=1;
rho1=0.540966;
rho2=-0.303792;
rho3=0.100791;
%
B0=1.9937718430;
B1=1.0985211604;
B2=-0.5094492996;
B3=-1.7619124270;
B4=-44.9005480267;
B5=-723692.2618632;
crholi=(0:56)/100; %mass fraction

%Density of water
tau1=1-teta;
rhoeauc=322; %(kg/m^3)
rhoeau=rhoeauc*(1+B0*tau1^(1/3)+B1*tau1^(2/3)+B2*tau1^(5/3)+B3*tau1^(16/3)+B4*tau1^(43/3)+B5*tau1^(110/3));

%Density of solution
rap=crholi./(1-crholi);
rholi=rhoeau*(rho0+rho1*rap+rho2*rap.^2+rho3*rap.^3); %kg/m3

%%%DENSITY OF KCl%%% (Darros-Barbosa, IJFP,6,2,195-214,2003
%Coefficients
T=25; %°C
a1=1.00199;
a2=-0.00011;
a3=-3.361e-6;
b1=0.003826;
b2=0.000135;
b3=-1.642e-6;
c1=0.000464;
c2=-2.616e-5;
c3=3.031e-7;
crhok=(0:10000)/1000; %g/0.1L
rhok=((a1+b1*crhok+c1*crhok.^2)+T*(a2+b2*crhok+c2*crhok.^2)+T^2*(a3+b3*crhok+c3*crhok.^2))*1000; %kg/cm^3

figure(2)
plot(crhona,rhona,'b');hold on;
plot(crhok,rhok,'r');hold on;
plot(crholi.*100,rholi,'g');


%%

%%%%%%%%%%%%%%%%%%%%%%%%%% REFRACTIVE INDEX %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%REFRACTIVE INDEX OF NaCl%%% (Tan, JCED, 2015, 60 ,2827-2833)
%wavelenght=589.3nm
%Coefficients
n1=1.3373;
n2=1.7682e-3;
n3=-5.8e-6;
n4=-1.3531e-4;
n5=-5.1e-8;
T=298.15;
cna=(0:260)/1000*100; %mass fraction (%)

nna=n1+n2*cna+n3*cna.^2+n4*(T-273.15)+n5*(T-273.15)^2; %Refractive index

%%%REFRACTIVE INDEX OF KCl%%% (Tan, JCED, 2015, 60 ,2827-2833)
%wavelenght=589.3nm
%Coefficients
n1=1.3352;
n2=1.6167e-3;
n3=-4e-7;
n4=-1.1356e-4;
n5=-5.7e-9;

ck=(0:150)/1000*100; %mass fraction (%)

nk=n1+n2*ck+n3*ck.^2+n4*(T-273.15)+n5*(T-273.15)^2; %Refractive index

%%%REFRACTIVE INDEX OF LiCl%%% Max,2001,J. Chem 79

%Density of water
tau1=1-teta;
rhoeauc=322; %(kg/m^3)
rhoeau=rhoeauc*(1+B0*tau1^(1/3)+B1*tau1^(2/3)+B2*tau1^(5/3)+B3*tau1^(16/3)+B4*tau1^(43/3)+B5*tau1^(110/3));

x=[1,2,4,9,12,15].*rhoeau/1000; %Penzkofer
y=[1.3414,1.3495,1.3652,1.3954,1.4256,1.4477];
n0=1.33413;
n1=0.00780;
x1=(0:140)/10;%mol/L
x2=n0+n1.*x1;

%plot
figure(3)
plot(cna,nna,'b');hold on;
plot(ck,nk,'r');hold on;

figure(33)
plot(x1,x2,'-','color','g');hold on
plot(x,y,'o','color','g')


%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%% OSMOTIC COEFFICIENT %%%%%%%%%%%%%%%%%%%%%%%
%T=25°C
%%%OSMOTIC COEFFICIENT OF NaCl%%% (Tang, JCIS, 114, 1986)
%T=25°C
%Coefficient
B0=1.370;
beta=2.796e-2;
C=4.803e-3;
D=-2.736e-4;
E=0;
A=0.5108;
cphina=(0:150)/10; %molality
mfna=1./(1+1./(cphina*Mmna));%mass fraction

phina=1-2.302585*(A/B0^3*1./cphina.*(1+B0*cphina.^(1/2)-4.60517*log10(1+B0*cphina.^(1/2)) ...
    -1./(1+B0*cphina.^(1/2)))-beta/2.*cphina-2/3*C.*cphina.^2-3/4*D.*cphina.^3-4/5*E.*cphina.^4);

%Osmotic coefficient from Hamer, JPCRD1, 1047,1972
B0=1.4495;
beta=2.0442e-2;
C=5.7927e-3;
D=-2.8860e-4;
A=0.5108;
cphina2=(0:60)/10; %molality
mfna2=1./(1+1./(cphina2*Mmna));%mass fraction
phina2=1-2.302585*(A/B0^3*1./cphina2.*(1+B0*cphina2.^(1/2)-4.60517*log10(1+B0*cphina2.^(1/2)) ...
    -1./(1+B0*cphina2.^(1/2)))-beta/2.*cphina2-2/3*C.*cphina2.^2-3/4*D.*cphina2.^3);
    
%%%OSMOTIC COEFFICIENT OF KCl%%% (Tang, JCIS, 114, 1986)
%T=25°C
%Coefficient
B0=1.350;
beta=-9.842e-3;
C=7.625e-3;
D=-7.892e-4;
E=2.492e-5;
A=0.5108;
cphik=(0:10000)/1000; %molality
mfk=1./(1+1./(cphik*Mmk)); %massfraction

phik=1-2.302585*(A/B0^3*1./cphik.*(1+B0*cphik.^(1/2)-4.60517*log10(1+B0*cphik.^(1/2)) ...
    -1./(1+B0*cphik.^(1/2)))-beta/2.*cphik-2/3*C.*cphik.^2-3/4*D.*cphik.^3-4/5*E.*cphik.^4);

%Osmotic coefficient from Hamer, JPCRD1, 1047,1972
B0=1.295;
beta=7e-5;
C=3.5990e-3;
D=-1.9540e-4;
A=0.5108;
cphik2=(0:5000)/1000; %molality
mfk2=1./(1+1./(cphik2*Mmk)); %massfraction
phik2=1-2.302585*(A/B0^3*1./cphik2.*(1+B0*cphik2.^(1/2)-4.60517*log10(1+B0*cphik2.^(1/2)) ...
    -1./(1+B0*cphik2.^(1/2)))-beta/2.*cphik2-2/3*C.*cphik2.^2-3/4*D.*cphik2.^3);

%%%OSMOTIC COEFFICIENT OF LiCl%%% (Hamer, JPCRD1, 1047,1972)
%T=25°C
%Coefficient
B0=1.6;
beta=8.5164e-2;
C=1.8335e-2;
D=-2.5742e-3;
A=0.5108;
cphili=(0:200)/10; %molality
mfli=1./(1+1./(cphili*Mmli)); %mass fraction

phili=1- ...
    2.302585*(A/B0^3*1./cphili.*(1+B0*cphili.^(1/2)-4.60517*log10(1+B0*cphili.^(1/2)) ...
    -1./(1+B0*cphili.^(1/2)))-beta/2.*cphili-2/3*C.*cphili.^2-3/4*D.*cphili.^3);


%Lietzke, JPC, 1962,Vol 66,3,508-509
%T=25°C
%Coefficient 
A=1.48996;
B=10.2909e-2;
C=6.04782e-3;
D=5.40012e-4;
S=1.17202;
cphili2=(0:500)/100; %mol/L
cmassli2=1./(1+1./(Mmli*cphili2));
%cmassli2=42.4e-3./rholi.*cphili2; %mass fraction

phili2=1-S/A^3*1./cphili2.*(1+A*cphili2.^(1/2)-2*log(1+A*cphili2.^(1/2))-1./(1+A*cphili2.^(1/2)))...
    +B*cphili2+C*cphili2.^2+D*cphili2.^3;


figure(4)
plot(mfna,phina,'b');hold on;
plot(mfk,phik,'r');hold on;
plot(mfna2,phina2,'b');hold on;
plot(mfk2,phik2,'r');hold on;
plot(cmassli2,phili2,'g');
%legend('NaCl','KCl','LiCl');

%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ACTIVITY OF SOLVENT %%%%%%%%%%%%%%%%%%%%
%T=25°C
%%%ACTIVITY OF SOLVENT FOR NaCl%%%
awna=exp(-phina.*cphina.*Mmwa*2); %molality

%%%ACTIVITY OF SOLVENT FOR LiCl%%%
Mw=18;
awli=exp(-phili.*cphili.*Mmwa*2); %molality

%%%ACTIVITY OF SOLVENT FOR KCl%%%
Mw=18;
awk=exp(-phik.*cphik.*Mmwa*2); %molality

figure(7)
plot(mfna,awna,'b');hold on;
plot(mfk,awk,'r');hold on;
ylabel('Activity of solvent'); xlabel('Mass fraction') 

%%

%%%%%%%%%%%%%%%%%%%%%%% HUMIDITY %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%HUMIDITY OF NaCl%%%
RHna=awna*100;

%%%HUMIDITY OF LiCl%%%
RHli=awli*100;

%%%HUMIDITY OF KCl%%%
RHk=awk*100;

figure(5);
plot(mfna,RHna,'b');hold on;
plot(mfk,RHk,'r');hold on;
%plot(mfli,RHli,'g');

%%

%%%%%%%%%%%%%%%%%%%%%%%%%%% MEAN ACTIVITY COEFFICIENT OF SOLUTE %%%%%%%%%%%%%%
%T=25°C
%%%ACTIVITY OF NaCl%%% (Tang, JCIS, 114,2,1986)
B0=1.370;
beta=2.796e-2;
C=4.803e-3;
D=-2.736e-4;
A=0.5108;
E=0;
cana=(0:14000)/1000; %molality
mfna=1./(1+1./(cana*Mmna));%mass fraction

ana=10.^(-A*cana.^(1/2)/(1+B0*cana.^(1/2))+beta*cana+C*cana.^2+D*cana.^3+E*cana.^4);

%%%ACTIVITY OF KCl%%% (Tang, JCIS, 114,2,1986)
B0=1.35;
beta=-9.842e-3;
C=7.625e-3;
D=-7.892e-4;
A=0.5108;
E=2.492e-5;
ck=(0:13000)/1000; %molality
mfk=1./(1+1./(ck*Mmk)); %massfraction

ak=10.^(-A*ck.^(1/2)/(1+B0*ck.^(1/2))+beta*ck+C*ck.^2+D*ck.^3+E*ck.^4);

%%%ACTIVITY OF LiCl%%% (Hamer, JPCRD1, 1047,1972)
B0=1.35;
beta=1.1603e-1;
C=-7.7726e-3;
D=2.9279e-3;
A=0.5108;
cli=(0:500)/100;
mfli=cli/Mmli./(1+1./(cli*Mmli)); %massfraction
ali1=10.^(-A*cli.^(1/2)/(1+B0*cli.^(1/2))+beta*cli+C*cli.^2+D*cli.^3);

%%Lietzke, JPC, 1962,Vol 66,3,508-509
A=1.48996;
B=10.2909e-2;
C=6.04782e-3;
D=5.40012e-4;
S=1.17202;
cphili2=(0:300)/100; %mol/L
cmassli2=1./(1+1./(Mmli*cphili2)); %mass fraction

ali=exp(-S*cphili2.^(1/2)./(1+A*cphili2.^(1/2))+2*B*cphili2+3/2*C*cphili2.^2+4/3*D*cphili2.^3);

figure(6)
plot(mfk,ak,'r');hold on
plot(mfna,ana,'b');hold on;
plot(cmassli2,ali,'g');hold on;
plot(mfli,ali1)



xli=[0.001,0.002,0.005,0.1,0.2,0.5,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9];
xli2=xli/42./(1+xli/42);
yli=[0.988,0.984,0.976,0.969,0.96,0.947,0.94,0.94,0.946,0.954,0.964,0.974,0.985,0.996,1.008];
figure(6)
plot(xli2,yli,'o')
% figure(7)
% set(gcf,'PaperUnits','centimeters') 
% set(gcf,'PaperPosition',[0.5 0.5 xSize ySize])
% set(gcf,'PaperSize',[xSize+1 ySize+1])
% grid on;
% % set(gca,'FontSize',20)
% set(gca,'Box','on')
% % ylim([1.24 1.41])
% % savename='SpectroIsothermPlot25June.fig';
% % savefig(savename)
% savename='ActivityLiCl.pdf';
% print(savename,'-dpdf') 