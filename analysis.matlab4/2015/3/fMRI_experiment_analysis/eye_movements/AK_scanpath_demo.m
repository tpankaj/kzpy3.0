
if not(exist('AK_3Oct2014_scanpaths'))
	load('/Users/davidzipser/Google Drive/Data/subjects/AK/2014/10/1Oct2014_freeviewing_stimVal/eye/Archive/AK_3Oct2014_scanpaths.735879.3506.mat')
end
blank = zeros(1024,1024,1,'single');

video_name = 'AK_3Oct2014_stimVal_scanpaths';
mkdir(d2s({'~/Desktop/' video_name '.' now}));
outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
outputVideo.FrameRate = 60;
outputVideo.Quality = 90;%75;%90;
open(outputVideo);

for i = 1:length(AK_3Oct2014_scanpaths)
	if ~strcmp(AK_3Oct2014_scanpaths(i).stimFile(1:10),'17.graysca')
		try
		stimulus = imread(d2s(...
			{'/Users/davidzipser/Google_Drive/Data/subjects/AK/2014/10/1Oct2014_freeviewing_stimVal/eye/Archive/Stimuli_selected_Validation_format-png/' ...
			AK_3Oct2014_scanpaths(i).stimFile}));
		stimulus = single(stimulus);
		mi(stimulus,1);
		hold on;
		x_eye = AK_3Oct2014_scanpaths(i).data4plot_x;
		y_eye = AK_3Oct2014_scanpaths(i).data4plot_y;
		plot(x_eye(1:1000),y_eye(1:1000),'.');
		hold off;
		axis([1,512,1,512]);

		fixspot = zeros(6,6,'single');
		fixspot(3:4,3:4) = 255;

		for j = 1:(1000/60):2000%(length(x_eye)-16)
			rj = round(j);
			x = mean(x_eye(rj:(rj+16)));
			y = mean(y_eye(rj:(rj+16)));
			if x > 0
				if x <= 512
					if y > 0
						if y <= 512
							e = place_img_A_in_img_B_v2(stimulus,blank+stimulus(1,1),256-y,256-x);
							e = place_img_A_in_img_B_v2(fixspot,e,0,0);
							e = e(356:668,306:718);
							e = zeroToOneRange(e);
							mi(e,2); title(round(j));
							writeVideo(outputVideo,e);
							drawnow();%pause(1/60);
						end
					end
				end
			end
		end %
		%my_pause
	catch me
		'Caught!'

	end
	end

end
close(outputVideo);