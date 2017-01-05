function my_dicom_to_nii( subject, year, month, session, protocol_name, runs )
%function my_dicom_to_nii( subject, year, month, session, protocol_name, runs )
%%%%%%% 5 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    fifty_path = '~/Data/osx/50';
    session_path = d2s({'~/Data/subjects/' subject '/' year '/' month '/' session});
    dcm_base_path = d2s({session_path '/dcm'});
    nii_path = d2s({session_path '/nii'});
    h=waitbar(0,'processing'); movegui(h,'southeast');
    for i = 1:length(runs)
        waitbar(i/length(runs));
        tic
        dcm_path = d2s({dcm_base_path '/' protocol_name runs(i) });
        system_str1 = d2s({ fifty_path ' -b ~/.dcm2niigui/dcm2niigui.ini ' dcm_path});
        fps(system_str1);
        system(system_str1);
        system_str2 = d2s({'mv ' dcm_path '/*.nii.gz ' nii_path});
        fps(system_str2);
        system(system_str2);
        toc
    end
    close(h);
    
end

