import javafx.application.Application; import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Label; import javafx.scene.paint.Color; import javafx.scene.input.MouseEvent; import javafx.scene.shape.Circle; import javafx.stage.Stage;
public class CircleColor extends Application{ public static void main(String[] ar){
launch(ar);
}
public void start(Stage stage){
Label l = new Label("Name: Darji Shivansh \nEnroll no.: 230410107124"); Circle c = new Circle(150,125,50);
Group group = new Group(l,c);
Scene scene = new Scene(group,300,250); 
c.setFill(Color.LIME); c.setOnMouseClicked(event -> {
c.setFill(Color.RED);
});
c.setOnMouseReleased(event -> { c.setFill(Color.BLUE);
});
stage.setTitle("Application_007"); stage.setScene(scene); stage.show();
}
}
