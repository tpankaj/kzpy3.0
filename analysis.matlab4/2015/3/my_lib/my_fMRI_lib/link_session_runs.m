function link_session_runs( subject, year, month, day )
% function link_session_runs( subject, year, month, day )
% e.g., link_session_runs('HVO',2015,2,18)
    clc

    start_dir = pwd;

    session_path = d2s({'~/Data/subjects/' subject '/' year '/' month '/' day});

    cd(session_path);

    if length(dir('runs'))>0
        error('runs folder exists.');
    end
    mkdir('runs');

    cd info;
    clear session_info;
    session_info;



    cd('../runs');

    for i = 1:length(session.runs)
        if length(session.runs(i).protocol) > 0
            session.runs(i)
            system(d2s({'mkdir ' i}));
            cd(d2s({i}));
            if length(session.runs(i).EyeLink_file) > 0
                if session.EyeLinkUsed == false
                    error('Unexpected EyeLink file.');
                end
                system(d2s({'ln -s ../../edf/' session.runs(i).EyeLink_file ' ' session.runs(i).EyeLink_file}));
            else
                if session.EyeLinkUsed == true
                    fps('*** WARNING! Lack EyeLink file!!!!!!!!!!!!');
                    my_pause;
                end
            end
            system(d2s({'ln -s ../../mat/' session.runs(i).mat_file ' ' session.runs(i).mat_file}));
            nifti_name = strrep(session.runs(i).nifti_file, '.nii.gz', '' );
            system(d2s({'ln -s ../../fsl/' session.runs(i).fsl_folder '/' nifti_name '.feat ' ...
                nifti_name '.feat'}));
            system(d2s({'ln -s ../../fsl/' session.runs(i).fsl_folder '/' nifti_name '.z_scored_filtered_func_data.mat ' ...
                nifti_name '.z_scored_filtered_func_data.mat'}));
            cd ..;
        end
    end

    cd(start_dir);

end

