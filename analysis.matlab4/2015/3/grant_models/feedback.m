function response = feedforward( fig_gnd, g3 )
    linear_s_g3 = conv(fig_gnd,g3);
    response = linear_s_g3;
    response(find(response<0))=0;
end

