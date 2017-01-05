function cimg = conformal_image( img )

    cimg = img * 0;
    N = 50;
    alpha = 0.345;
    width = length(img);
    hwidth = width / 2;
    
    for x = 250:257
        for y = 250:257
            img(x,y) = 255;
        end
    end
    for x = 1:width
        for y = 1:width
            [xdeg, ydeg, orientation, eccentricity] = visual_coordinates_from_512px_vim1_fixated_image( x, y );
            X = hwidth;
            Y = hwidth;

            if eccentricity > 0
                X = X + alpha * 25 * exp(eccentricity/3) * cos(orientation / 360 * 2 * pi);
                Y = Y + alpha * 25 * exp(eccentricity/3) * -sin(orientation / 360 * 2 * pi);
            end
            X = round(X);
            Y = round(Y);
            if true
            if X < 1
                X = 1;
            end
            if Y < 1
                Y = 1;
            end
            if X > 512
                X = 512;
            end
            if Y > 512
                Y = 512;
            end
            end
            cimg(x, y) = img(X, Y);
        end
    end
    
    
end

