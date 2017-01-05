function [selectedImages, Xs, Ys, displayMatrix ] = displayCellArrayOfPicturesAndClick( imageList, strList, paddingFactor, fig, figTitle, num_clicks )
%function [selected_image_list, Xs, Ys, displayMatrix ] = displayCellArrayOfPicturesAndClick( imageList, strList, paddingFactor, fig, figTitle, doClicking )
%   24 Dec. 2013
    
    slist = {};
    for i = 1:length(imageList)
        s = imageList{i};
        newWidth = ceil(length(s)*(1+2*paddingFactor));
        newStart = round(length(s)*paddingFactor);
        sPadded = zeros( newWidth, newWidth );
        sPadded( (newStart+1):(newStart+length(s)),(newStart+1):(newStart+length(s))) = s;
        slist{i} = sPadded;
    end
    clear s;

    maxWidth = 0;
    for i = 1:length(slist)
        if length(slist{i}) > maxWidth
            maxWidth = length(slist{i});
        end
    end

    roundSqrtLength = ceil(sqrt(length(slist)));


    displayMatrix = zeros(maxWidth*roundSqrtLength,maxWidth*roundSqrtLength,'single');

    j = 1;
    k = 1;
    textListXYs = [];
    for i = 1:length(slist)
        if j > roundSqrtLength
            j = 1;
            k = k + 1;
        end
        displayMatrix((1+(k-1)*maxWidth):(k*maxWidth),(1+(j-1)*maxWidth):(j*maxWidth)) = slist{i};
        textListXYs(i,:) = [ paddingFactor*maxWidth+(k-1)*maxWidth, paddingFactor*maxWidth+(j-1)*maxWidth ];
        j = j + 1;
    end

    figure(fig);hold off;
    mi(displayMatrix,fig,[1,1,1]);
    axis('off');
    my_title( figTitle );
    if length( strList ) > 0
        for i = 1:length(slist)
            text( textListXYs(i,2), textListXYs(i,1), strList(i), 'Color',[0.6,0.3,0.3]);
        end
    end
    
    pause(0.01);

    selected_image_list = [];
    
    Xs = [];
    Ys = [];
    selectedImages = [];
    if num_clicks > 0
        
        'click to select, return to go on or end.'
        for clicks = 1:num_clicks
            figure(fig);
            [x,y] = ginput(1);
            if length(x)<1
                break;
            end
            
            hold on; plot(x,y,'r.'); hold off;
            imagesX = floor(x/maxWidth);
            imagesY = floor(y/maxWidth);
            localX = x - imagesX*maxWidth;
            localY = y - imagesY*maxWidth;

            hold on; plot(imagesX*maxWidth+localX,imagesY*maxWidth+localY,'bx'); hold off;

            selectedImages(clicks) = (imagesY)*roundSqrtLength + imagesX + 1;
%            selectedImages
            Xs(clicks) = localX-newStart;
            Ys(clicks) = localY-newStart;
        end
        
%         for i = 1:length(selectedImages)
%             selImg = selectedImages(i);
%             selected_image_list = [selected_image_list, str2num(strList{selImg}) ];
%         end
    
    end
    
    
    
end
