// import javafx.application.Application; 
// import javafx.scene.Group;
// import javafx.scene.Scene;
// import javafx.scene.control.Label; import javafx.scene.image.ImageView; 
// import javafx.scene.image.Image; 
// import javafx.scene.layout.GridPane; 
// import javafx.scene.layout.VBox; 
// import javafx.stage.Stage;
// public class Tictactoe extends Application{ public static void main(String[] ar){ launch(ar);
// }
// public void start(Stage stage){ GridPane gp = new GridPane(); VBox hb = new VBox();
// Label l = new Label("Name: Darji Shivansh          Enroll no.: 230410107124"); for(int i = 0; i<3; i++){
// for(int j = 0; j<3; j++){
// int choice = (int)(Math.random()*3); if(choice == 0)
// gp.add(new ImageView(new Image("file:C:/Users/SHIVANSH/Desktop/Java/images/zerob.png")),i,j); else if(choice == 1)
// gp.add(new ImageView(new Image("file:C:/Users/SHIVANSH/Desktop/Java/images/xb.png")),i,j); else
// continue;
// }
// }
// gp.setGridLinesVisible(true); hb.getChildren().addAll(l,gp);
// Scene scene = new Scene(hb,500,550); stage.setTitle("My JavaFX Application"); stage.setScene(scene);
// stage.show();
// }
// }
// import javafx.application.Application; 
// import javafx.scene.Group;
// import javafx.scene.Scene;
// import javafx.scene.control.Label; 
// import javafx.scene.image.ImageView; 
// import javafx.scene.image.Image; 
// import javafx.scene.layout.GridPane; 
// import javafx.scene.layout.VBox; 
// import javafx.stage.Stage;
// public class Tictactoe extends Application{ public static void main(String[] ar){ launch(ar);
// }
// public void start(Stage stage){ GridPane gp = new GridPane(); VBox hb = new VBox();
// Label l = new Label("Name: Darji Shivansh \nEnroll no.: 230410107124"); for(int i = 0; i<3; i++){
// for(int j = 0; j<3; j++){
// int choice = (int)(Math.random()*3); if(choice == 0){
// ImageView iv = new ImageView(new Image("file:C:/Users/SHIVANSH/Desktop/Java/images/zerob.jpg"));
// iv.setFitWidth(80);iv.setFitHeight(80);gp.add(iv,i,j);}else if(choice == 1){
// ImageView iv = new ImageView(new Image("file:C:/Users/SHIVANSH/Desktop/Java/images/xb.png"));
// iv.setFitWidth(80);iv.setFitHeight(80);gp.add(iv,i,j);}else
// continue;
// }
// }
// gp.setGridLinesVisible(true); hb.getChildren().addAll(l,gp);
// Scene scene = new Scene(hb,300,350); stage.setTitle("My JavaFX Application"); stage.setScene(scene);
// stage.show();
// }
// }

import javafx.application.Application; 
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Label; 
import javafx.scene.image.ImageView; 
import javafx.scene.image.Image; 
import javafx.scene.layout.GridPane; 
import javafx.scene.layout.VBox; 
import javafx.stage.Stage;
public class Tictactoe extends Application{ public static void main(String[] ar){ launch(ar);
}
public void start(Stage stage){ GridPane gp = new GridPane(); VBox hb = new VBox();
Label l = new Label("Name: Darji Shivansh \nEnroll no.: 230410107124"); for(int i = 0; i<3; i++){
for(int j = 0; j<3; j++){
int choice = (int)(Math.random()*3); if(choice == 0){
ImageView iv = new ImageView(new Image("file:C:/Users/SHIVANSH/Desktop/Java/images/zerob.jpg"));
iv.setFitWidth(80);iv.setFitHeight(80);gp.add(iv,i,j);}else if(choice == 1){
ImageView iv = new ImageView(new Image("file:C:/Users/SHIVANSH/Desktop/Java/images/xb.png"));
iv.setFitWidth(80);iv.setFitHeight(80);gp.add(iv,i,j);}else
continue;
}
}
gp.setGridLinesVisible(true); hb.getChildren().addAll(l,gp);
Scene scene = new Scene(hb,300,350); stage.setTitle("My JavaFX Application"); stage.setScene(scene);
stage.show();
}
}