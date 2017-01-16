function FVM_3Jan2014_750am(voxels, movement_rule, top_8_correlations_indicies, top_8_correlations_values, GRAPHICS, run_version )
% FVM(voxels, movement_rule)
%
% e.g. FVM_3Jan2015_750am(voxel_set, 'rule2', top_correlations_indicies, top_correlations_values, true, '2Jan2014_first_run' )
% 30 Dec. 2014 beginning functional voxel mapping work (again).
% 6 Jan 2015 photos version
% e.g. FVM_6Jan2015_photos(1:1750, 'rule2', top_correlations_indicies, top_correlations_values, true, '6Jan2014_photo_run1' )
%%%%%%%%%%%%%
% 3 January 2015
% To use this to work from a saved vox_xys file, do the following:
%
% local_startup
% G_initalize
% load('/Users/internetaccess/Desktop/Matlab_Desktop/high_snr_1p5_voxel_correlations.735966.0987.mat')
% voxel_correlations = high_snr_1p5_voxel_correlations;
% nb_3Jan2015
% % e.g. a particular vox_xys file:
% load('/Users/internetaccess/Desktop/Matlab_Desktop/2Jan2014_first_run.735967.3223.vox_xys.mat')
% G.vox_xys = vox_xys;
% N = length(voxel_set);
% vox_position_matrix = zeros(2*N,2*N,'single');
% for i = 1:N
%     x = vox_xys(i,1);
%     y = vox_xys(i,2);
%     vox_position_matrix(x,y) = voxel_set(i);
% end
% G.vox_position_matrix = vox_position_matrix;
% 
% Then uncomment the lines where vox_position_matrix and vox_xys come from
% G.
%
% FVM_3Jan2014_750am(voxel_set, 'rule2', top_correlations_indicies, top_correlations_values, true, '2Jan2014_first_run' )
%
% All of this needs to be improved.
%
% FVM_4Jan2015_1208pm(voxel_set, 'rule2', top_correlations_indicies, top_correlations_values, true, '4Jan2014_run2' )
%
%%%%%%%%%%%%%%%%%

    %GRAPHICS = 0;
    global vox_xys;
    global vox_position_matrix;
    global G;
    
% Uncomment these to get values in first time from G.
%     vox_position_matrix=G.vox_position_matrix; 
%     vox_xys=G.vox_xys;

    E = G.constants.KAY_2008;
    V = G.constants.NOV_2013_COMBINED_TRIALS;
    VAL = G.constants.VAL;
    TRN = G.constants.TRN;
    if GRAPHICS
        S = G.e(E).v(V).s(1);
        roi = S.roi;
        roiColors = [1 1 0; 1 0 0; 1 0.3 0.3; 1 0.6 0.6; 0.4 0.4 1; 0 0 1; 0.3 1 0.3; 0 1 0];
    end
   
    
    
%     if nargin < 2
%         voxels = 1:256;
%         movement_rule = 'rule1';
%     end
    
    N = length(voxels);
    %vox_position_matrix = []; % temp, to run first time, if value already set.
    size(vox_position_matrix)
    if length(vox_position_matrix) < 1
        [vox_xys, vox_position_matrix] = FVM_initalize( voxels );
    end
    display_matrix = zeros(length(vox_position_matrix),length(vox_position_matrix),3,'single');
    display_matrix2 = zeros(length(vox_position_matrix),length(vox_position_matrix),1,'single');

    for k = 1:1000
        tic
        if GRAPHICS
            randVal = randi(120);%31;%1505;%1563;%1665;%
            %randVal=k;
            mi(get_Kay_image('Val',randVal),3,[1,1,1],d2s({randVal}));
        end
        ctr = 0;
        jMAX = 100;
        for j = 1:jMAX
            ctr = ctr + 1;
            if ctr > 10
                ctr = 1;
            end
            fprintf('.');
            
            switch movement_rule
                case 'rule1'
                    [vox_xys vox_position_matrix] = FVM_move_rule1( voxels, vox_xys, vox_position_matrix );
                case 'rule2'
                    [vox_xys vox_position_matrix] = FVM_move_rule2( voxels, vox_xys, vox_position_matrix, top_8_correlations_indicies, top_8_correlations_values);
                case 'dont_move'
                    'okay'
                otherwise
                    error('otherwise');
            end

            if and(j==jMAX,GRAPHICS)
                display_matrix(:,:,1) = 0*vox_position_matrix;
                display_matrix(:,:,2) = 0*vox_position_matrix;
                display_matrix(:,:,3) = 0*vox_position_matrix;
                display_matrix2 = 0 * display_matrix2;
                for i = 1:N
                    if ismember(i,G.people)
                        face = 1;
                        place = 0;                      
                        other = 0;
                    elseif ismember(i,G.places)
                        face = 0;
                        place = 1;
                        other = 0;
                    elseif ismember(i,G.flat)
                        face = 0;
                        place = 0;
                        other = 1;
                    elseif ismember(i,G.animals)
                        face = 1;
                        place = 1;
                        other = 0;
                    else
                        face = 0.5;
                        place = 0.5;
                        other = 0.5;
                    end
                    %if S.roi(voxels(i)) == 2
                    xy = vox_xys(i,:);
                    z_score = 1;%S.stim(VAL).data(voxels(i),randVal);
                    if z_score > 3
                        z_score = 3;
                    elseif z_score < -3
                        z_score = -3;
                    end
                    display_matrix2(xy(1),xy(2)) = z_score;%S.stim(VAL).data(voxels(i),randVal);
                    %if ctr > S.roi(voxels(i))
                    display_matrix(xy(1),xy(2),:) = [face place other];%roiColors( 1+S.roi(voxels(i)),:);%1+S.roi(voxels(i));
                    %end
                    %end
                end
                %mi(vox_position_matrix,1,[1,2,1],d2s({sum(sum(vox_position_matrix))}));
                %a = round(2*3*N/10); b = round(2*7*N/10);
                a = round(2*4.7*N/10); b = round(2*5.3*N/10);
                A = vox_position_matrix(a:b,a:b);
                A(find(A==0)) = median(voxels);
                %mi(A,1,[1,2,1],d2s({j}));
                %display_matrix(a,a,2) = 8;
                mi(display_matrix2(a:b,a:b,1),1,[1,2,1],d2s({ctr-1}));
                mi(display_matrix(a:b,a:b,:),1,[1,2,2],d2s({ctr-1}));

                drawnow;%pause(0.01)
                %pause
            end
        end
        
        fprintf(' Saving vox_xys\n');
        my_save(vox_xys, 'vox_xys', d2s({run_version '.' now '.vox_xys'}));
 %return       
        [vox_xys vox_position_matrix] = FVM_breath_space( voxels, vox_xys, vox_position_matrix, 2 );
        toc
    end
end

% initialize positions
function [vox_xys vox_position_matrix] = FVM_initalize( voxels )
    fprintf('FVM_initalize\n');
    %error('here');
    N = length(voxels);

    vox_xys = zeros(N,2,'single');
    vox_position_matrix = zeros(2*N,2*N,'single');

    vox_position_matrix = 0 * vox_position_matrix;
    for i = 1:N
        while true
            x = randi(N) + round(N/2);
            y = randi(N) + round(N/2);
            if ~vox_position_matrix(x,y)
                vox_position_matrix(x,y) = voxels(i);
                vox_xys(i,:) = [x y];
                break;
            end
        end
    end
end

% % move voxels according to some rule
% function [vox_xys vox_position_matrix] = FVM_move_rule1( voxels, vox_xys, vox_position_matrix )
%     N = length(voxels);
%     for i = 1:N
%         xy = vox_xys(i,:);
%         dx = round((voxels(i)-N/2)/80+rand(1)*(N-xy(1)+5*randn(1))/20);%randi(3)-2;
%         dy = round((voxels(i)-N/2)/80+rand(1)*(N-xy(2)+5*randn(1))/20);%randi(3)-2;
% %         dx = round(rand(1)*(N-xy(1)+5*randn(1))/10);%randi(3)-2;
% %         dy = round(rand(1)*(N-xy(2)+5*randn(1))/10);%randi(3)-2;
%         if or(or( xy(1)+dx >= 1, xy(1)+dx <= 2*N ),or( xy(2)+dy >= 1, xy(2)+dy <= 2*N ))
%             if ~vox_position_matrix(xy(1)+dx,xy(2)+dy)
%                 vox_xys(i,1)=vox_xys(i,1)+dx;
%                 vox_xys(i,2)=vox_xys(i,2)+dy;
%                 vox_position_matrix(xy(1)+dx,xy(2)+dy)=voxels(i);
%                 vox_position_matrix(xy(1),xy(2))=0;
%             end
%         end
%     end
% end

function [vox_xys vox_position_matrix] = FVM_move_rule2( voxels, vox_xys, vox_position_matrix, top_8_correlations_indicies, top_8_correlations_values)
    N = length(voxels);
    rnx = 30*randn(1);
    rny = 30*randn(1);
    for j = 1:N
        i = randi(N);
        xy_center = [0 0];
        correlated_voxels = top_8_correlations_indicies(i,:);
        for j = 1:length(correlated_voxels)
            %[correlated_voxels(j) size(vox_xys)]
            cxy = vox_xys(correlated_voxels(j),:);
            xy_center = xy_center + cxy * top_8_correlations_values(i,j);
        end
        xy_center = xy_center / sum(top_8_correlations_values(i,:));
        xy = vox_xys(i,:);
        dxy = round((0.1*randn(1,2)+((3*[N+rnx N+rny]+xy_center)/4 - xy)/1)/25);
        %if not(or(or(min(xy+dxy)<1),or(max(xy+dxy)>2*N)))
            if ~vox_position_matrix(xy(1)+dxy(1),xy(2)+dxy(2))
                vox_xys(i,1)=vox_xys(i,1)+dxy(1);
                vox_xys(i,2)=vox_xys(i,2)+dxy(2);
                vox_position_matrix(xy(1)+dxy(1),xy(2)+dxy(2))=voxels(i);
                vox_position_matrix(xy(1),xy(2))=0;
            end            
        %end
    end
end


% breath space into center voxels, and suffle outer voxels
function [vox_xys vox_position_matrix] = FVM_breath_space( voxels, vox_xys, vox_position_matrix, expansion_factor )
    N = length(voxels);
    vox_position_matrix = 0 * vox_position_matrix;
    mx = median(vox_xys(:,1));
    my = median(vox_xys(:,2));
    for i = 1:N
        vox_xys(i,:) = round([N N] + expansion_factor * (vox_xys(i,:) - [mx my]));
    end
    for i = 1:N
        xy = vox_xys(i,:);
        if or(or( xy(1) < 1, xy(1) > 2*N ),or( xy(2) < 1, xy(2) > 2*N ))
            while true
                x = randi(2*N);
                y = randi(2*N);
                if ~vox_position_matrix(x,y)
                    vox_position_matrix(x,y) = voxels(i);
                    vox_xys(i,:) = [x y];
                    break;
                end
            end
        end
    end
end
