// Set Measurment parameters
run("Set Measurements...", "area shape feret's display redirect=None decimal=3");

// Get a list of all image titles
imageTitles = getList("image.titles");

for (i = 0; i < imageTitles.length; i++) {
    // Select image by title
    selectImage(imageTitles[i]);
    title = getTitle();
    
    // Split the title into organoid and focus parts
    splitTitle = split(title, "_");   
    Ba = splitTitle[0]; // "Batch"
    Dy = splitTitle[3]; // "Dy"
    DyNum = parseInt(replace(Dy, "[^0-9]", ""));
    Stitch = splitTitle[6]; //"Stitched status"
    
    //Identify image details, resize images and add scale
    if(Stitch == "stitched"){
	   	//Run Dialog
		Dialog.create("Resize");
		Dialog.addMessage("Pixel Size Values for: "+title);
		Dialog.addNumber("Pixel Width", "");
		Dialog.addNumber("Pixel Height", "");
		Dialog.show();
		
		//Get values
		width = Dialog.getNumber();
		height = Dialog.getNumber();
		
		//Resize and Scale
		run("Size...", "width="+width+" height="+height+" depth=1 average interpolation=None");
		run("Set Scale...", "distance=1128 known=2778 unit=um");
    }else{
	    if(Ba == "BA1"){
	    	if(DyNum == 24){
	    		run("Size...", "width=2048 height=1536 depth=1 average interpolation=None");
				run("Set Scale...", "distance=446 known=1000 unit=um");
	    	}else if(DyNum < 17){
	    		run("Size...", "width=1128 height=832 depth=1 average interpolation=None");
				run("Set Scale...", "distance=1128 known=1903 unit=um");
			}else{
			run("Size...", "width=1128 height=832 depth=1 average interpolation=None");
			run("Set Scale...", "distance=1128 known=2778 unit=um");
			}
	    }else if(Ba == "BA3"){
	    		run("Size...", "width=1920 height=1440 depth=1 average interpolation=None");
				run("Set Scale...", "distance=1920 known=3629 unit=um");
		}else if(DyNum < 17){
	    		run("Size...", "width=1128 height=832 depth=1 average interpolation=None");
				run("Set Scale...", "distance=1128 known=1903 unit=um");
	    		}else{
	    		run("Size...", "width=1128 height=832 depth=1 average interpolation=None");
				run("Set Scale...", "distance=1128 known=2778 unit=um");
	    		}
    }		
    		//Run measuremnts
			setThreshold(1, 255);
			setOption("BlackBackground", true);
			run("Convert to Mask");
			run("Create Selection");
			run("Analyze Particles...", "size=90000-Infinity circularity=0-1.00 display include");
			close();
}