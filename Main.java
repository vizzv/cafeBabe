import java.util.Scanner;

public final class Main implements xx,vv{
    static final int mainV=50;
    public final static String dV="cafeBabe";
    static final Float y=30.01f;
    
    private static double x;
    static Integer a =50;
    public final static float ff=1.0f;
    public static void methodd(){
        System.out.println(dV+x);
    }
    public static void methodd(int aa){
        System.out.println(dV+x+aa);
    }
    
    private static class ku6b{
        int ku6bv=0;
    }
    private static class vizzly extends node implements vv,xx{
        int a;
        String v;
        
        public static void hidimba(boolean b){ System.out.println("hihihihihihi");}
        public static int xeroOrone(boolean b){return b?1:0;}
        public static void hidimba1(boolean b){ System.out.println("hihihihihihi1");}
        public static int xeroOrone1(boolean b){return b?1:0;}
    }
    node vvvv= new node(1234, null);
    public static void hidimba(boolean b){ System.out.println("hihihihihihi");}
    public static int xeroOrone(boolean b){return b?1:0;}

    static int staticInteger=0;
    
    public static void main(String[] args) throws Exception
    {   
        System.out.println(ff);
        System.out.println("enter kk");
        
        Scanner sc= new Scanner(System.in);
        int kk=sc.nextInt();
        System.out.println(kk);
        sc.close();
        a:{
            System.out.println("i am in a");
        }
        System.out.println("namaste!!!");
        
        node v=new node(1,new node());
        vizzly vzz= new vizzly();
        vzz.a=5;
        vzz.hidimba(false);
        treeNode root=new treeNode(1, new treeNode(), new treeNode());
        System.out.println(v.head+"->"+v.next.next);
        System.out.print(root.left.value);
        System.out.println(mainV);
        System.out.println(y);
        treeNode rr= createTree(); 
        methodd();
        Main.ku6b k= new ku6b();
        k.ku6bv=2;
        System.out.println(rr);
        System.out.println(50+19);
    }

    public static treeNode createTree(){
        treeNode treeRoot=new treeNode();
        treeRoot.left= new treeNode();
        treeRoot.right=new treeNode();
        return treeRoot;
    }
    public static treeNode createTree(treeNode leftt,treeNode rightt){
        treeNode treeRoot=new treeNode();
        treeRoot.left= leftt;
        treeRoot.right=rightt;
        return treeRoot;
    }
    
}
interface vv{
    public static void hidimba(boolean b){ System.out.println("hihihihihihi");}
    public static int xeroOrone(boolean b){return b?1:0;}
}
interface xx{
    public static void hidimba1(boolean b){ System.out.println("hihihihihihi");}
    public static int xeroOrone1(boolean b){return b?1:0;}
}
class node implements xx{
    int head;
    node next;
    node(int head,node next){
        this.head=head;
        this.next=next;
    }
    node(){
        this.next=null;
    }
    public static void hidimba(boolean b){ System.out.println("hihihihihihi");}
    public static int xeroOrone(boolean b){return b?1:0;}
    public static int getValue(node root){
        return root.head;
    }
}
final class treeNode{
    int value;
    treeNode left;
    treeNode right;
    treeNode(){
    }
    treeNode(int val,treeNode lft,treeNode rght){
        this.value=val;
        this.left=lft;
        this.right=rght;
    }
}