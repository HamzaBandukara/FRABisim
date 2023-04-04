package ProcessElement;

import org.antlr.v4.runtime.misc.Pair;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class RawProcess {

   public int children;
   public RawProcess[] childProcess;
   public Set<Integer> support;
   public Set<Integer> names;
   private int hash;
   protected String strForm;

   public String toString(){
      setUpStrForm();
      return strForm;
   };

   protected void setUpStrForm(){
   }

   public Set<Integer> getNames(){return names;}
   public Set<Integer> getSupport(){return support;}

   public RawProcess(){
      support = new HashSet<>();
      names = new HashSet<>();
      strForm = null;
   }

   public RawProcess generator(String s){
      if(Character.isLowerCase(s.charAt(0))){
         return null;
      }
      return null;
   }

   public void setChildren(RawProcess[] kids) throws Exception {
      if(kids.length != children){
         throw new Exception("Not correct number of child processes.");
      }
      this.childProcess = kids;
   }

   public Set<Pair<String, RawProcess>> OneStep(){
      return null;
   }

   public void SetUpRP(){
      for(RawProcess rp: childProcess){
         support.addAll(rp.support);
      }
      for(RawProcess rp: childProcess)
         names.addAll(rp.names);
   }

    public RawProcess rewrite(int key, int n1) {
       return null;
    }

   public RawProcess ReFix(Map<Integer, Integer> nameMap) {
      return null;
   }

    public String strBuilder(Map<Integer, Integer> nameMap) {
      System.out.println("BAD CALL");
      return "";
    }
}

