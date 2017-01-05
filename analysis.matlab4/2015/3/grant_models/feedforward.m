function response = feedforward( stimulus, gn100 )
    linear_s_gn100 = conv(stimulus,gn100);
    response = linear_s_gn100;
    response(find(response<0))=0;
end