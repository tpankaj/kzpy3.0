function FVM(voxels, movement_rule, top_8_correlations_indicies, top_8_correlations_values, GRAPHICS )
% FVM(voxels, movement_rule)
%
% e.g., FVM(voxel_set, 'rule2', top_correlations_indicies, top_correlations_values, false )
% 30 Dec. 2014 beginning functional voxel mapping work (again).
    %GRAPHICS = 0;
    global vox_xys;
    global vox_position_matrix;
    global G;
%     vox_position_matrix=G.vox_position_matrix;
%     vox_xys=G.vox_xys;
    E = G.constants.KAY_2008;
    V = G.constants.NOV_2013_COMBINED_TRIALS;
    VAL = G.constants.VAL;
    TRN = G.constants.TRN;
    if GRAPHICS
        S = G.e(E).v(V).s(1);
    end
    
    display_matrix = 0*vox_position_matrix;
    
%     if nargin < 2
%         voxels = 1:256;
%         movement_rule = 'rule1';
%     end
    
    N = length(voxels);
    size(vox_position_matrix)
    if length(vox_position_matrix) < 1
        [vox_xys, vox_position_matrix] = FVM_initalize( voxels );
    end

    for k = 1:100
        tic
        if GRAPHICS
            randVal = randi(120);%31;%1505;%1563;%1665;%
            %randVal=k;
            mi(get_Kay_image('Val',randVal),2,[1,1,1],d2s({randVal}));
        end
        for j = 1:100
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

            if GRAPHICS%and(j==100,GRAPHICS)
                display_matrix = 0*vox_position_matrix;
                for i = 1:N
                    %if S.roi(voxels(i)) == 2
                    xy = vox_xys(i,:);
                    z_score = S.stim(VAL).data(voxels(i),randVal);
                    if z_score > 3
                        z_score = 3;
                    elseif z_score < -3
                        z_score = -3;
                    end
                    display_matrix(xy(1),xy(2)) = z_score;%S.stim(VAL).data(voxels(i),randVal);
                    %end
                end
                %mi(vox_position_matrix,1,[1,2,1],d2s({sum(sum(vox_position_matrix))}));
                %a = round(2*3*N/10); b = round(2*7*N/10);
                a = round(2*4.85*N/10); b = round(2*5.15*N/10);
                A = vox_position_matrix(a:b,a:b);
                A(find(A==0)) = median(voxels);
                mi(A,1,[1,2,1],d2s({j}));
                mi(display_matrix(a:b,a:b),1,[1,2,2],d2s({randVal}));
                drawnow;%pause(0.01)
                %pause
            end
        end
        fprintf('\n');
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

% move voxels according to some rule
function [vox_xys vox_position_matrix] = FVM_move_rule1( voxels, vox_xys, vox_position_matrix )
    N = length(voxels);
    for i = 1:N
        xy = vox_xys(i,:);
        dx = round((voxels(i)-N/2)/80+rand(1)*(N-xy(1)+5*randn(1))/20);%randi(3)-2;
        dy = round((voxels(i)-N/2)/80+rand(1)*(N-xy(2)+5*randn(1))/20);%randi(3)-2;
%         dx = round(rand(1)*(N-xy(1)+5*randn(1))/10);%randi(3)-2;
%         dy = round(rand(1)*(N-xy(2)+5*randn(1))/10);%randi(3)-2;
        if or(or( xy(1)+dx >= 1, xy(1)+dx <= 2*N ),or( xy(2)+dy >= 1, xy(2)+dy <= 2*N ))
            if ~vox_position_matrix(xy(1)+dx,xy(2)+dy)
                vox_xys(i,1)=vox_xys(i,1)+dx;
                vox_xys(i,2)=vox_xys(i,2)+dy;
                vox_position_matrix(xy(1)+dx,xy(2)+dy)=voxels(i);
                vox_position_matrix(xy(1),xy(2))=0;
            end
        end
    end
end

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
        dxy = round((0.1*randn(1,2)+((1*[N+rnx N+rny]+xy_center)/2 - xy)/1)/25);
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

