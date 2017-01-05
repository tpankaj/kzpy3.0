run Data_loading_script_vim1_S1.m

rf19214=get_rf_image(19214);

if true % example
    X1 = log(0.001):0.1:log(12);
    X1 = exp(X1);
    Y1 = 0*X1+0.00001;
    R = (-3.1/2):0.1:(3.2/2);
    Rn = R;
    E = 0*R+0.2;
    for i = 1:12
        E = [E,0*R+i];
        Rn = [Rn,R];
    end
    R = Rn;


    X2 = E.*cos(R);
    Y2 = E.*sin(R);

    X3 = log(0.001):0.5:log(12/sqrt(2));
    X3 = exp(X3);
    
    X = [X1,Y1,X3,X3,Y1,X2];
    Xn = -X;
    Y = [Y1,X1,X3,-X3,-X1,Y2];
    X = [X,Xn];
    Y = [Y,Y];

    Xrfs512 = [];
    Yrfs512 = [];
    Xrfs = [];
    Yrfs = [];
    rf_counter = 0;
    for v = 1:length(all_voxels_measured_peaks_512px)
        %if and(or(all_voxels_roi_int_codes(v) == 1,all_voxels_roi_int_codes(v) == 1), all_voxels_measured_peaks_512px(v,1))
        if and(true, all_voxels_measured_peaks_512px(v,1))
            rf_counter = rf_counter + 1;
            x = all_voxels_measured_peaks_512px(v,1);
            y = all_voxels_measured_peaks_512px(v,2);
            [xdeg,ydeg] = visual_coordinates_from_512px_vim1_fixated_image( x, y );
            Xrfs512 = [Xrfs512,x];
            Yrfs512 = [Yrfs512,y];
            Xrfs = [Xrfs,xdeg];
            Yrfs = [Yrfs,ydeg];
        end
    end
end
    
    figure(1);subplot(1,3,1);hold off;subplot(1,3,2);hold off;subplot(1,3,3);hold off;
    mi(rf19214,1,[1,3,1]); hold on;
    for i = 1:length(Xrfs)
        plot(Xrfs512(i),Yrfs512(i),'ro');%,'MarkerSize',0.1);
    end
    plot(all_voxels_measured_peaks_512px(19214,1),all_voxels_measured_peaks_512px(19214,2),'b.');
    subplot(1,3,2);
    for i = 1:length(Xrfs)
        plot(Xrfs(i),-Yrfs(i),'ro');hold on;
    end
    
    for i = 1:length(X)
        plot(X(i),Y(i),'.','MarkerSize',0.1);hold on;
    end

    axis('square');axis([-15,15,-15,15]);
    
            
    subplot(1,3,3);
    for i = 1:length(Xrfs) 
        [u,v] = vector_in_cortex_plane( Xrfs(i), -Yrfs(i) );
        plot(u,v,'ro');hold on;
    end
    for i = 1:length(X) 
        [u,v] = vector_in_cortex_plane( X(i), Y(i) );
        plot(u,v,'o','MarkerSize',0.1);hold on;
    end
    
    axis('square');axis([-1.2,1.2,-1.2,1.2]);
