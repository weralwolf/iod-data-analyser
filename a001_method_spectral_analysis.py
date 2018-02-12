from os.path import join

from matplotlib import pyplot as plt
from numpy import round, abs, array

from iod.a000_config import DE2_NACS_DIR, DE2_WATS_DIR
from iod.a000_config import NFFT
from ionospheredata.method import break_points
from ionospheredata.method import gravitation_wave
from ionospheredata.parser import FileParser
from ionospheredata.parser import NACSRow, WATSRow


def main():
    nacs_datafile = '1982327T164000_0_DE2_NACS_1S_V01.ASC'
    nacs_data = FileParser(NACSRow, join(DE2_NACS_DIR, nacs_datafile))

    # Separate parameters to different dataset
    ut_nacs = round(nacs_data.get('ut', transposed=True)[0] / 1000.)  # from `ms` to `s`
    oxigen = nacs_data.get('o_dens', transposed=True)[0]  # 1/cm^3
    nitrogen = nacs_data.get('n2_dens', transposed=True)[0]  # 1/cm^3
    orbit = nacs_data.get('orbit', transposed=True)[0][0]  # No.

    # Looking for breaking point (BP) in NACS nacs_data
    sampling_NACS = 1
    bps = break_points(ut_nacs, sampling_NACS)

    # NACS_O
    if len(bps) > 1:
        O = oxigen[:int(bps[1, 0])]  # why is it impotant?.. if I need not full nacs_data set
        N2 = nitrogen[:int(bps[1, 0])]
        ut_nacs_1sec = ut_nacs[:int(bps[1, 0])]  # all UT nacs_data in NACS with 1 sec from start to breake point
    else:
        O = oxigen[:int(bps[0, 1])]
        N2 = nitrogen[:int(bps[0, 1])]
        ut_nacs_1sec = ut_nacs[:int(bps[0, 1])]
    L_Ox = len(O)  # length of nacs_data set after BP ... so length of nacs_data have changed

    # function create trend and detect GW
    Trend_O, Wave_O, FFT_GW_O, GravWave_Oxigen = gravitation_wave(O)
    Trend_N2, Wave_N2, FFT_GW_N2, GravWave_Nitrogen = gravitation_wave(N2)

    # figure % nacs_data from SC, trend and GW in Oxigen and Nitrogen

    # Concentration and trend for O and N2
    # ut = list(ut_nacs)
    # gca = plt.subplot(2, 2, 1)
    # plt.plot(ut, O, color='r')
    # plt.plot(ut, Trend_O[:L_Ox], 'm')
    # plt.plot(ut, N2, 'g')
    # plt.plot(ut, Trend_N2[:L_Ox], 'c')
    # plt.legend(
    #     ('Oxigen', 'Oxigen trend', 'Nitrogen', 'Nitrogen trend'),
    #     loc='upper right'
    # )
    # plt.grid(True)
    # plt.xlabel('UT, s')
    # plt.ylabel('Concentration, 1/cm^3')
    # plt.title('{}. Orbit #{} UT start {}h'.format(nacs_datafile[7:14], int(orbit), int(ut[0]) // 3600))
    # gca.set_xlim(xmin=min(ut_nacs), xmax=max(ut_nacs))

    # # O and N2 spectrum
    # gca = plt.subplot(2, 2, 2)
    # plt.plot(range(NFFT), abs(FFT_GW_O), 'r')
    # plt.plot(range(NFFT), abs(FFT_GW_N2), 'g')
    # plt.legend(
    #     ('Oxigen', 'Nitrogen')
    # )
    # plt.grid(True)
    # plt.title('Gravitation wave spectrum')
    # gca.set_xlim(xmin=0, xmax=2600)

    # # iFFT wave in GW area in O and N2 nacs_data
    # gca = plt.subplot(2, 1, 2)
    # print(GravWave_Oxigen)
    # plt.plot(abs(GravWave_Oxigen), 'r')
    # plt.plot(abs(GravWave_Nitrogen), 'g')
    # plt.title('Gravitation wave area (from spectrum')
    # plt.legend(
    #     ('Oxigen', 'Nitrogen'),
    #     loc='upper left'
    # )
    # plt.show()

    #    fpath=['E:\Sciense\DISER\work in Matlab\programs\METHODICS_2016\ ',dayOrbit];
    #    filename=[dayOrbit,'_O-N_2'];
    # saveas(gcf, fullfile(fpath,filename),'jpeg');
    #     saveas(gcf, fullfile(fpath,filename),'pdf');

    # WATS
    wats_datafile = '1982327_de2_wats_2s_v01.asc'
    print(join(DE2_WATS_DIR, wats_datafile))
    wats_data = FileParser(WATSRow, join(DE2_WATS_DIR, wats_datafile))

    mode = wats_data.get('mode', transposed=True)[0]
    vmode = array(list(map(lambda m: m == 5 or m == 6, mode)))
    hmode = array(list(map(lambda m: m == 3 or m == 4, mode)))

    vsc = wats_data.get('v_sc', transposed=True)[0]
    vz = vsc * vmode  # m/s
    vy = vsc * hmode  # m/s
    wats_ut = round(wats_data.get('ut', transposed=True)[0] / 1000.)  # ms
    temperature = wats_data.get('tn', transposed=True)[0]  # K

    # % Harmonization of data NACS and WATS by UT
    # [Vz_start]=Aria_WATS(UT_NACS_1sec(1), UT_WATS_Vz);
    # [Vz_end]=UT_WATS_end_point(UT_NACS_1sec(end), UT_WATS_Vz);

    # %Looking for breake poins there
    # sampling_WATS_Vz=8;
    # [breake_points_Vz]=BreakePoints(UT_WATS_Vz(Vz_start:Vz_end), sampling_WATS_Vz);

    # if (length(breake_points_Vz(:,1))>1) && (breake_points_Vz(2,1)~=breake_points_Vz(1,1))
    #         Vz_end=Vz_start+breake_points_Vz(2,1)-1;
    # elseif (length(breake_points_Vz(:,1))==1) || (breake_points_Vz(2,1)==breake_points_Vz(1,1))
    #         Vz_end=Vz_end;
    # end

    #     Vz=VerticalWind(Vz_start:Vz_end);
    #     T_Vz=Temperature_Vz(Vz_start:Vz_end);
    #         L_Vz=UT_WATS_Vz(Vz_end)-UT_WATS_Vz(Vz_start); % how many seconds lost ... so how long should be data set
    #         Length_Vz=length(Vz); % carent data set with sampling = 8 second
    # [Vz_interpolated]=Naiquist_theorem(Vz, L_Vz, Length_Vz);
    # [T_Vz_interpolated]=Naiquist_theorem(T_Vz, L_Vz, Length_Vz);

    #      UT_WATS_Vz_1sec=(UT_WATS_Vz(Vz_start):1:UT_WATS_Vz(Vz_end-1))'; % each one second from the startVz to endVz

    # [Trend_Vz, wave_Vz, FFT_Vz, FFT_GW_Vz, GravWave_Vz]=GravitationWave_Wind(Vz_interpolated);
    #     L_Vz=length(Vz_interpolated);
    # [Trend_T_Vz, wave_T_Vz, FFT_dT_Vz, FFT_GW_T_Vz, dT]=GravitationWave_Wind(T_Vz_interpolated);
    #         dTnorm=[dT(1:L_Vz)./Trend_T_Vz(1:L_Vz); zeros(2^16-L_Vz,1)];

    # %% Horizontal wind (Vy)
    # [WATS_Vy]=Horizontal_wind_WATS(K_wats);

    #     HorizontalWind=WATS_Vy(:,12); % [m/s]
    #         UT_WATS_HorizWind=WATS_Vy(:,2); % [ms]
    #     UT_WATS_Vy=round(UT_WATS_HorizWind./1000); % [sec]
    #     Temperature_Vy=WATS_Vy(:,6);
    #     Latitude_WATS_Vy=WATS_Vy(:,16);

    # [Vy_start]=Aria_WATS(UT_NACS_1sec(1), UT_WATS_Vy);
    #         [Vy_end]=UT_WATS_end_point(UT_NACS_1sec(end), UT_WATS_Vy);

    #         UT_WATS_Vy_bp=UT_WATS_Vy(Vy_start:2:Vy_end);
    #         sampling_WATS_Vy=8;
    #         [breake_points_Vy]=BreakePoints(UT_WATS_Vy_bp, sampling_WATS_Vy);

    # if length(breake_points_Vy(:,1))>1
    #         Vy_end=Vy_start+breake_points_Vy(2,1)*2-1;
    # else
    #         Vy_end=Vy_end;
    # end
    # % Axis of Vy changen when satellite cross poles
    # %...so we nead take into account this fact
    # Vy=HorizontalWind(Vy_start:2:Vy_end);
    # Lat_Vy=Latitude_WATS_Vy(Vy_start:2:Vy_end);

    # [Vy_corr]=Vy_correction(Vy, Lat_Vy);

    #         T_Vy=Temperature_Vy(Vy_start:Vy_end);
    #       L_Vy=UT_WATS_Vy(Vy_end)-UT_WATS_Vy(Vy_start); % how many seconds lost
    #       Length_Vy=length(Vy_corr);

    # [Vy_interpolated]=Naiquist_theorem(Vy_corr, L_Vy, Length_Vy);
    #      UT_WATS_Vy_1sec=(UT_WATS_Vy(Vy_start):1:UT_WATS_Vy(Vy_end))';

    # [Trend_Vy, wave_Vy, FFT_Vy, FFT_GW_Vy, GravWave_Vy]=GravitationWave_Wind(Vy_interpolated);

    # figure % Vy and Vy_correct coz Vy axe change direction
    #     subplot(211), plot(1:length(Vy),Vy,'r','LineWidth',2); grid on
    #         set(gca,'XLim',[0 length(Vy)]);
    #     subplot(212), plot(1:length(Vy),Vy_corr,'r','LineWidth',2); grid on
    #         set(gca,'XLim',[0 length(Vy)]);
    #         xlabel('Vy and Vy_correction coz of Y axe change direction','fontsize',12);
    #         title(['Datafile   ' dayOrbit  '   Orbit Nomber  ' num2str(Orbit(1)) '   UT start   ' num2str(UT_NACS(1)/3600) 'hour'],'fontsize',14);

    #    filename=[dayOrbit,'_Vy'];
    # saveas(gcf, fullfile(fpath,filename),'jpeg');
    #     saveas(gcf, fullfile(fpath,filename),'pdf');


    # figure % Wind and Temperature
    #     % Vz
    #         subplot(321), plot(1:length(Vz_interpolated),Vz_interpolated,'b','LineWidth',1); grid on
    #             hold on
    #         subplot(321), plot(1:L_Vz,Trend_Vz(1:L_Vz),'c','LineWidth',1);
    #             hold on
    #         subplot(321), plot(1:L_Vz,wave_Vz(1:L_Vz),'b','LineWidth',2);
    #                 set(gca,'XLim',[0 length(Vz_interpolated)]);
    #                 xlabel('Vz (blue line)','fontsize',12);
    #                 title(['Datafile' '   ' dayOrbit  '   ' 'Noises in data from NACS'],'fontsize',14);
    #         % FFT Vz-Trend
    #         subplot(322), plot(1:2^16,abs(FFT_Vz),'b','LineWidth',2); grid on
    #                 set(gca,'XLim',[0 2600]);
    #     % Vy
    #         subplot(323), plot(1:length(Vy_interpolated),Vy_interpolated,'r','LineWidth',1); grid on
    #             hold on
    #         subplot(323), plot(1:L_Vy,Trend_Vy(1:L_Vy),'m','LineWidth',1);
    #             hold on
    #         subplot(323), plot(1:L_Vy,wave_Vy(1:L_Vy),'r','LineWidth',2);
    #                 set(gca,'XLim',[0 length(Vy_interpolated)]);
    #                 xlabel('Vy (red line)','fontsize',12);

    #         % FFT Vy-Trend
    #         subplot(324), plot(1:2^16,abs(FFT_Vy),'r','LineWidth',2); grid on
    #                 set(gca,'XLim',[0 2600]);
    #     % T
    #         subplot(325), plot(1:length(T_Vz_interpolated),T_Vz_interpolated,'m','LineWidth',2); grid on
    #             hold on
    #         subplot(325), plot(1:length(T_Vz_interpolated),Trend_T_Vz(1:length(T_Vz_interpolated)),'m','LineWidth',2);
    #             hold on
    #         subplot(325), plot(1:length(T_Vz_interpolated),wave_T_Vz(1:length(T_Vz_interpolated)),'r','LineWidth',2);
    #                 set(gca,'XLim',[0 length(T_Vz_interpolated)]);
    #                 xlabel('Temperature','fontsize',12);
    #         % FFT T
    #         subplot(326), plot(1:2^16,abs(FFT_dT_Vz),'m','LineWidth',2); grid on
    #                 set(gca,'XLim',[0 2600]);
    #                 xlabel('SPECTRUM of parameters','fontsize',12);
    #                 title(['Datafile   ' dayOrbit  '   Orbit Nomber  ' num2str(Orbit(1)) '   UT start   ' num2str(UT_NACS(1)/3600) 'hour'],'fontsize',14);

    #      filename=[dayOrbit,'_Vy_Vz_T'];
    # saveas(gcf, fullfile(fpath,filename),'jpeg');
    #     saveas(gcf, fullfile(fpath,filename),'pdf');


    # %% dz
    # [dz, FFT_dz]=Vertical_displacement_dz(Temperature_Vz(Vz_start:Vz_end), GravWave_Oxigen, GravWave_Nitrogen, L_Ox);

    # %[Trend_dz, Wave_dz, FFT_wave_dz, FFT_GW_dz, GravWave_dz]=GravitationWave_Wind(dz');

    # figure %4  dp/p and dz
    #     % dz_normalised
    #     subplot(221), plot(1:length(dz), dz,'k','LineWidth',2); grid on
    #         hold on
    #             set(gca,'XLim',[0 length(dz)]);
    #             xlabel('dz','fontsize',12);
    #     subplot(222), plot(1:NFFT, abs(FFT_dz),'k','LineWidth',2); grid on
    #             set(gca,'XLim',[0 2600]);
    #             xlabel('Spectrum dz','fontsize',12);

    #             %% dp/p = (dO+dN2)/(trendO+trendN2)+dT/T
    #     % p=nkT: n - from NACS (each 1 sec); T - from WATS (each 8 sec)
    #     % for coherence of dO/O, dN2/N2 and dT/T fluctuations
    #     for i_NACS=1:length(UT_NACS_1sec)
    #         if UT_WATS_Vz_1sec(1)==UT_NACS_1sec(i_NACS)
    #             s=i_NACS; % startNACS
    #         end
    #         if UT_WATS_Vz_1sec(end)==UT_NACS_1sec(i_NACS)
    #             e=i_NACS; % endNACS
    #         end
    #     end

    # [dp_p, FFT_GW_dp]=PressureVariation(Wave_O(s:e), Wave_N2(s:e), Trend_O(s:e), Trend_N2(s:e), dT(1:length(UT_WATS_Vz_1sec)));
    #     % dp_p
    #     subplot(223), plot(1:length(dp_p), dp_p,'m','LineWidth',2); grid on
    #             set(gca,'XLim',[0 length(dp_p)]);
    #             xlabel('dp','fontsize',12);
    #     subplot(224), plot(1:NFFT,abs(FFT_GW_dp),'m','LineWidth',2); grid on
    #             set(gca,'XLim',[0 2600]);
    #             xlabel('Spectrum dp','fontsize',12);
    #             title(['Datafile   ' dayOrbit  '   Orbit Nomber  ' num2str(Orbit(1)) '   UT start   ' num2str(UT_NACS(1)/3600) 'hour'],'fontsize',14);

    #    filename=[dayOrbit,'_dz_dp'];
    # saveas(gcf, fullfile(fpath,filename),'jpeg');
    #     saveas(gcf, fullfile(fpath,filename),'pdf');


    # figure % Spectrum of all parameters
    #     plot(0:2^16-1, abs(FFT_GW_O).*1e-10,'r','LineWidth',2); grid on
    #         hold on
    #     plot(0:2^16-1, abs(FFT_GW_N2).*1e-10,'g','LineWidth',2);
    #         hold on
    #     plot(1:2^16,abs(FFT_Vz).*1e-4,'b','LineWidth',2);
    #         hold on
    #     plot(1:2^16,abs(FFT_Vy).*1e-4,'m','LineWidth',2);
    #         hold on
    #     plot(1:2^16,abs(FFT_GW_T_Vz).*1e-5,'r','LineWidth',1);
    #         hold on
    #     plot(1:2^16,abs(FFT_dz).*1e-6,'k','LineWidth',2);
    #         hold on
    #     plot(1:2^16,abs(FFT_GW_dp).*1e-4,'c','LineWidth',2);
    #         set(gca,'XLim',[0 3020],'YLim',[0 4]);
    #         xlabel('O (red), N2 (green), Vz (blue), Vy (magenta), T (red thik), dz (black), dp (cyant)','fontsize',12);
    #         title(['Datafile   ' dayOrbit  '   Orbit Nomber  ' num2str(Orbit(1)) '   UT start   ' num2str(UT_NACS(1)/3600) 'hour'],'fontsize',14);

    #    filename=[dayOrbit,'_all_spectrum'];
    # saveas(gcf, fullfile(fpath,filename),'jpeg');
    #     saveas(gcf, fullfile(fpath,filename),'pdf');

    # %% NOISE calculate in fraquencies aria

    #                 Poit100km=round(2^16*7.8/100);% 100 km - bottom line of GW
    #             mN=mean(abs(FFT_GW_O(Poit100km:2^16-Poit100km)));
    # for i=1:2^16
    #     Noise(i)=mN;
    # end
    #         for i_noise=[1:Poit100km-1, 2^16-Poit100km+1:2^16]
    #             FFT_noise(i_noise)=mN;
    #         end
    #         for i_noise=Poit100km:2^16-Poit100km
    #             FFT_noise(i_noise)=FFT_GW_O(i_noise);
    #         end

    #         ifft_noise=ifft(FFT_noise);
    #                 ifft_Oxigen=ifft(FFT_GW_O);
    #                 for_persent_calcul=max(real(ifft_Oxigen));


    # figure % Noise in spectr - all scales less 100 km
    #         subplot(311), plot(0:2^16-1,abs(FFT_GW_O(1:2^16)),'r','LineWidth',1); grid on
    #             hold on
    #         subplot(311), plot(0:2^16-1, Noise,'m','LineWidth',2);
    #                 set(gca,'XLim',[0 2600], 'YLim', [0 max(abs(FFT_GW_O(1:2^16)))/10]);
    #                 xlabel('Oxigen (red line), Noise (magenta line)','fontsize',12);
    #                 title(['Datafile' '   ' dayOrbit  '   ' 'Noises in data from NACS'],'fontsize',14);

    #         subplot(312), plot(1:L_Ox,real(ifft_noise(1:L_Ox)),'m','LineWidth',2); grid on
    #                 set(gca,'XLim',[0 L_Ox]);
    #                 xlabel('Noise from Oxigen data','fontsize',12);
    #                 title(['Datafile   ' dayOrbit  '   Orbit Nomber  ' num2str(Orbit(1)) '   UT start   ' num2str(UT_NACS(1)/3600) 'hour'],'fontsize',14);

    # % Histogramm of NOISE
    #                 x=linspace(min(real(ifft_noise(1:L_Ox))), max(real(ifft_noise(1:L_Ox))),100);
    #         subplot(313), hist(real(ifft_noise(1:L_Ox)), x); grid on
    #                  xlabel('Noise from Oxigen data','fontsize',12);

    #    filename=[dayOrbit,'_Noises'];
    # saveas(gcf, fullfile(fpath,filename),'jpeg');
    #     saveas(gcf, fullfile(fpath,filename),'pdf');

if __name__ == '__main__':
    main()
