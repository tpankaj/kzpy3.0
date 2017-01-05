function img = get_Kay_image( stimSet_str, img_num )
%function img = get_Kay_image( stimSet_str, img_num )
%   e.g., mi(get_Kay_image('Trn',1),1,[1,2,1]);mi(get_Kay_image('Val',1),1,[1,2,2]);
global G;

        if strcmp(stimSet_str,'Trn')
            img = sqsing(G.stimTrn512_int8(img_num,:,:));
        elseif strcmp(stimSet_str,'Val')
            img = sqsing(G.stimVal512_uint8(img_num,:,:));
        else
            error;
        end
end

