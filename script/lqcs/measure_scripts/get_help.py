def export_help_to_file(obj, filename='object_methods.txt', recursive=True, 
                       include_methods=True, include_private=False):
    """
    将对象的帮助信息导出到文件，按照类层次结构（从基类到子类）和方法顺序组织
    """
    import sys
    from io import StringIO
    import inspect
    
    # 设置标准输出的编码
    if hasattr(sys.stdout, 'encoding'):
        original_encoding = sys.stdout.encoding
    else:
        original_encoding = None
    
    try:
        # 使用utf-8编码打开文件
        with open(filename, 'w', encoding='utf-8') as f:
            # 保存原来的stdout
            old_stdout = sys.stdout
            
            # 获取对象的类
            obj_class = obj if inspect.isclass(obj) else obj.__class__
            
            # 获取所有相关的类（按照MRO顺序，从基类到子类）
            classes_to_process = []
            if recursive:
                # 反转MRO顺序，从基类开始到最终子类
                classes_to_process = list(reversed(get_all_parent_classes(obj_class)))
            else:
                classes_to_process = [obj_class]
            
            # 写入总体信息
            f.write("OBJECT HELP EXPORT - CLASS HIERARCHY (BASE TO DERIVED)\n")
            f.write("="*80 + "\n\n")
            f.write(f"Target object: {obj}\n")
            f.write(f"Final class: {obj_class.__name__}\n")
            f.write(f"Total classes in hierarchy: {len(classes_to_process)}\n")
            f.write(f"Export time: {get_current_time()}\n\n")
            
            # 为每个类生成帮助信息（从基类到子类）
            for i, cls in enumerate(classes_to_process):
                # 写入类分隔符和信息标题
                f.write("\n" + "#"*80 + "\n")
                f.write(f"CLASS {i+1}/{len(classes_to_process)}: {cls.__name__}\n")
                f.write(f"Hierarchy level: {i} ({'Base' if i == 0 else 'Derived'})\n")
                f.write(f"Module: {cls.__module__}\n")
                f.write("#"*80 + "\n\n")
                
                # 先获取并写入类的帮助信息
                sys.stdout = class_stdout = StringIO()
                
                # 临时设置stdout的编码
                try:
                    if hasattr(sys.stdout, 'reconfigure'):
                        sys.stdout.reconfigure(encoding='utf-8')
                except:
                    pass
                
                # 获取类的帮助信息
                help(cls)
                
                # 恢复stdout并获取内容
                sys.stdout = old_stdout
                class_help = class_stdout.getvalue()
                
                # 写入类帮助信息
                f.write("CLASS OVERVIEW:\n")
                f.write("-"*40 + "\n")
                f.write(class_help)
                f.write("\n")
                
                # 如果包含方法详细信息
                if include_methods:
                    # 按照方法名称排序获取方法帮助信息
                    save_methods_help(cls, f, include_private, class_index=i+1, total_classes=len(classes_to_process))
            
            # 写入总结信息
            f.write("\n" + "="*80 + "\n")
            f.write("EXPORT SUMMARY\n")
            f.write("="*80 + "\n")
            f.write(f"Total classes processed: {len(classes_to_process)}\n")
            f.write(f"Export completed at: {get_current_time()}\n")
            
            print(f"帮助信息已保存到: {filename}")
            print(f"按照类层次结构处理了 {len(classes_to_process)} 个类")
            
    except Exception as e:
        print(f"保存文件时出错: {e}")
    finally:
        # 恢复原来的编码
        if original_encoding and hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding=original_encoding)
            except:
                pass

def save_methods_help(cls, file_obj, include_private=False, class_index=1, total_classes=1):
    """
    保存类的所有方法的详细帮助信息，按照方法名称排序
    """
    import sys
    from io import StringIO
    import inspect
    
    # 获取所有方法并按名称排序
    methods = sorted(get_class_methods(cls, include_private))
    
    if not methods:
        file_obj.write("No methods found in this class.\n\n")
        return
    
    file_obj.write(f"\n{'='*60}\n")
    file_obj.write(f"METHODS IN {cls.__name__} ({len(methods)} methods, "
                  f"Class {class_index}/{total_classes})\n")
    file_obj.write(f"{'='*60}\n\n")
    
    old_stdout = sys.stdout
    
    for i, method_name in enumerate(methods, 1):
        try:
            method = getattr(cls, method_name)
            
            # 方法标题
            file_obj.write(f"\n{'~'*50}\n")
            file_obj.write(f"Method {i}/{len(methods)}: {method_name}\n")
            file_obj.write(f"{'~'*50}\n\n")
            
            # 方法基本信息
            file_obj.write(f"Method type: {get_method_type(method)}\n")
            
            # 获取方法签名
            try:
                sig = inspect.signature(method)
                file_obj.write(f"Signature: {sig}\n\n")
            except (ValueError, TypeError):
                file_obj.write("Signature: Unable to get signature\n\n")
            
            # 获取方法文档字符串
            doc = inspect.getdoc(method)
            if doc:
                file_obj.write("DOCUMENTATION:\n")
                file_obj.write("-" * 40 + "\n")
                file_obj.write(f"{doc}\n\n")
            else:
                file_obj.write("Documentation: No docstring available\n\n")
            
            # 获取完整的帮助信息
            sys.stdout = method_stdout = StringIO()
            try:
                if hasattr(sys.stdout, 'reconfigure'):
                    sys.stdout.reconfigure(encoding='utf-8')
                help(method)
                method_help = method_stdout.getvalue()
                file_obj.write("FULL HELP INFORMATION:\n")
                file_obj.write("-" * 40 + "\n")
                file_obj.write(f"{method_help}\n")
            except:
                file_obj.write("Full help: Unable to get help information\n")
            finally:
                sys.stdout = old_stdout
            
            # 获取源代码（如果可用）
            try:
                source = inspect.getsource(method)
                file_obj.write("\nSOURCE CODE:\n")
                file_obj.write("-" * 40 + "\n")
                file_obj.write(f"{source}\n")
            except (TypeError, OSError):
                pass  # 对于内置方法无法获取源代码
            
            file_obj.write("\n" + "."*50 + "\n\n")
            
        except Exception as e:
            file_obj.write(f"Error processing method {method_name}: {e}\n\n")
    
    sys.stdout = old_stdout

def get_method_type(method):
    """获取方法的类型"""
    import inspect
    if inspect.ismethod(method):
        return "Bound method"
    elif inspect.isfunction(method):
        return "Function"
    elif isinstance(method, property):
        return "Property"
    elif callable(method):
        return "Callable"
    else:
        return "Unknown"

def get_class_methods(cls, include_private=False):
    """
    获取类的所有可调用方法，按照方法类型分类
    """
    import inspect
    
    methods = []
    for name in dir(cls):
        # 跳过魔术方法和私有方法（除非特别指定）
        if not include_private:
            if name.startswith('_') and not name.startswith('__') and not name.endswith('__'):
                continue
            if name.startswith('__') and name.endswith('__') and name not in [
                '__init__', '__str__', '__repr__', '__len__', '__getitem__',
                '__setitem__', '__delitem__', '__iter__', '__next__', '__call__'
            ]:
                continue
        
        try:
            attr = getattr(cls, name)
            if (callable(attr) or inspect.ismethod(attr) or 
                inspect.isfunction(attr) or isinstance(attr, property)):
                methods.append(name)
        except:
            continue
    
    return methods

def get_all_parent_classes(cls):
    """
    获取类的所有父类（包括自身），按照MRO顺序
    """
    try:
        return list(cls.__mro__)
    except AttributeError:
        return [cls]

def get_current_time():
    """获取当前时间字符串"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def export_class_hierarchy_diagram(obj, filename='class_hierarchy.txt'):
    """
    导出类的继承层次结构图
    """
    import inspect
    
    obj_class = obj if inspect.isclass(obj) else obj.__class__
    all_classes = list(reversed(get_all_parent_classes(obj_class)))  # 从基类到子类
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("CLASS HIERARCHY DIAGRAM (BASE → DERIVED)\n")
        f.write("="*50 + "\n\n")
        
        for i, cls in enumerate(all_classes):
            indent = "  " * i
            arrow = "→ " if i < len(all_classes) - 1 else "✓ "
            
            f.write(f"{indent}{arrow}{cls.__name__}\n")
            f.write(f"{indent}   │ Module: {cls.__module__}\n")
            
            # 获取类文档的第一行
            doc = inspect.getdoc(cls)
            if doc:
                first_line = doc.split('\n')[0].strip()
                f.write(f"{indent}   └─ Documentation: {first_line[:80]}...\n")
            
            f.write(f"{indent}   \n")  # 空行
            
        f.write(f"\nTotal hierarchy levels: {len(all_classes)}\n")
        f.write(f"Base class: {all_classes[0].__name__}\n")
        f.write(f"Derived class: {all_classes[-1].__name__}\n")

def export_structured_help(obj, filename='structured_help.txt'):
    """
    结构化的帮助信息导出，按照类层次和方法分类
    """
    import inspect
    
    obj_class = obj if inspect.isclass(obj) else obj.__class__
    all_classes = list(reversed(get_all_parent_classes(obj_class)))  # 从基类到子类
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("STRUCTURED HELP EXPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Object: {obj}\n")
        f.write(f"Class hierarchy: {len(all_classes)} levels\n\n")
        
        # 类层次结构概览
        f.write("CLASS HIERARCHY:\n")
        f.write("-"*40 + "\n")
        for i, cls in enumerate(all_classes):
            f.write(f"{i+1}. {cls.__name__} ({cls.__module__})\n")
        f.write("\n")
        
        # 每个类的详细方法信息
        for cls_idx, cls in enumerate(all_classes):
            f.write(f"\n{'#'*60}\n")
            f.write(f"CLASS {cls_idx+1}: {cls.__name__}\n")
            f.write(f"{'#'*60}\n\n")
            
            # 类文档
            class_doc = inspect.getdoc(cls)
            if class_doc:
                f.write("CLASS DOCUMENTATION:\n")
                f.write("-"*40 + "\n")
                f.write(f"{class_doc}\n\n")
            
            # 方法列表
            methods = sorted(get_class_methods(cls, include_private=False))
            if methods:
                f.write(f"PUBLIC METHODS ({len(methods)}):\n")
                f.write("-"*40 + "\n")
                for method in methods:
                    f.write(f"• {method}\n")
                f.write("\n")
            
            # 方法详细信息（只显示签名和文档）
            for method_name in methods:
                method = getattr(cls, method_name)
                f.write(f"{method_name}:\n")
                f.write("-"*30 + "\n")
                
                try:
                    sig = inspect.signature(method)
                    f.write(f"  Signature: {sig}\n")
                except:
                    f.write("  Signature: N/A\n")
                
                doc = inspect.getdoc(method)
                if doc:
                    # 只取第一行文档
                    first_line = doc.split('\n')[0]
                    f.write(f"  Description: {first_line.strip()}\n")
                
                f.write("\n")

# 使用示例
if __name__ == "__main__":
    # 示例：使用自定义类层次
    class BaseClass:
        """基类"""
        def base_method(self):
            """基类方法"""
            pass
        
        def common_method(self):
            """通用方法"""
            pass
    
    class IntermediateClass(BaseClass):
        """中间类"""
        def intermediate_method(self):
            """中间类方法"""
            pass
        
        def common_method(self):
            """重写的通用方法"""
            pass
    
    class FinalClass(IntermediateClass):
        """最终类"""
        def final_method(self):
            """最终类方法"""
            pass
        
        def special_method(self, param1, param2=None):
            """
            特殊方法
            
            Args:
                param1: 第一个参数
                param2: 可选参数
            """
            pass
    
    # 创建实例并导出帮助
    obj = FinalClass()
    
    # 导出完整的层次化帮助信息
    export_help_to_file(obj, 'hierarchical_help.txt', 
                       recursive=True, include_methods=True, include_private=False)
    
    # 导出类层次结构图
    export_class_hierarchy_diagram(obj, 'class_hierarchy_diagram.txt')
    
    # 导出结构化摘要
    export_structured_help(obj, 'structured_summary.txt')
    
    print("导出完成！文件已按照类层次结构组织。")