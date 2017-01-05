function r = neural_response(s1,s2,sfg,satt,gn100_transient, gn100_sustained, g3, g_attention, max_time_ms)
    K1=0.25;
    resting_rate = 0.0005;
    r1_transient = feedforward( s1, gn100_transient );
    r1_sustained = feedforward( s1, gn100_sustained )-K1*r1_transient;
    r2_transient = feedforward( s2, gn100_transient );
    r2_sustained = feedforward( s2, gn100_sustained )-K1*r2_transient;
    fg1 = feedback( sfg, g3 );
    attn = feedback( satt, g_attention );
    r1_transient = r1_transient(1:max_time_ms)+resting_rate;
    r1_sustained = r1_sustained(1:max_time_ms)+resting_rate;
    r2_transient = r2_transient(1:max_time_ms)+resting_rate;
    r2_sustained = r2_sustained(1:max_time_ms)+resting_rate;
    fg1 = fg1(1:max_time_ms);
    attn = attn(1:max_time_ms);
    r = r1_transient+r2_transient+r1_sustained+r2_sustained+fg1.*(r1_sustained+1*r2_sustained ) + attn/100;
end