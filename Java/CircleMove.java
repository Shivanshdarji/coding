import javafx.application.Application; import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Label; import javafx.scene.input.KeyCode; import javafx.scene.shape.Circle; import javafx.stage.Stage;
public class CircleMove extends Application{ public static void main(String[] ar){ launch(ar);
}
public void start(Stage stage){
Label l = new Label("Name: Darji Shivansh \nEnroll no.: 230410107124"); Circle c = new Circle(250,250,50);
Group group = new Group(c);
Scene scene = new Scene(group,500,550); scene.setOnKeyPressed(event -> { if(event.getCode() == KeyCode.UP){ c.setCenterY(c.getCenterY()-50);
}else if(event.getCode() == KeyCode.DOWN){ c.setCenterY(c.getCenterY()+50);
}else if(event.getCode() == KeyCode.RIGHT){ c.setCenterX(c.getCenterX()+50);
}else if(event.getCode() == KeyCode.LEFT){ c.setCenterX(c.getCenterX()-50);
}
});
stage.setTitle("My JavaFX Application"); stage.setScene(scene);
stage.show();
}
}
