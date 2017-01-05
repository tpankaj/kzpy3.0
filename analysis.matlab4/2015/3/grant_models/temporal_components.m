function [gn100_transient, gn100_sustained, g_fig_gnd, g_attention] = temporal_components()

    max_time_ms = 1000;
    t = (1:max_time_ms)/max_time_ms;
    tn = t.^(1/4);
    tn100 = round(1000*tn(1:5:max_time_ms));

    %%%%%%%%%%%%% transient response waveform %%%%%%%%%%%%%
    g_fast = gaussian(1:max_time_ms,max_time_ms/2,max_time_ms/30);
    g_fast = g_fast(tn100);
    g_slow = gaussian(1:length(tn100),80,50);
    gn100_transient = g_fast-g_slow/8;
    k = 35;
    gn100_transient(k:(length(tn100)-1))=gn100_transient(1:(length(tn100)-k));
    gn100_transient(1:(k+5))=0;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%%%%%%%%% sustained response waveform %%%%%%%%%%%%%
    %g_sustained = gaussian(1:max_time_ms,max_time_ms/2,max_time_ms/10);
    %g2_sustained = gaussian(1:length(tn100),60,40);
    gn100_sustained = (g_fast-g_slow/30)/4;
    gn100_sustained(k:(length(tn100)-1))=gn100_sustained(1:(length(tn100)-k));
    gn100_sustained(1:(k+4))=0;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%%%%%%%%% modulation response waveform %%%%%%%%%%%%%
    g_fig_gnd = gaussian(1:(2*length(tn100)),130,15);
    g_attention = gaussian(1:(2*length(tn100)),250,60);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
	if 1    
        mp({g_fast},101,[3,3,1],'g_fast');
        mp({g_slow},101,[3,3,2],'g_slow');
        mp({gn100_transient},101,[3,3,3],'gn100_transient');
        mp({gn100_sustained},101,[3,3,6],'gn100_sustained');
        mp({g_fig_gnd},101,[3,3,7],'g_fig_gnd');
        mp({g_attention},101,[3,3,8],'g_attention');
    end
end