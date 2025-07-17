#!/usr/bin/env python3
"""
Script para forzar el registro de filtros de Jinja2
"""

def register_filters_manually(app):
    """Registra todos los filtros manualmente"""
    
    def safe_sum_filter(values, attribute=None):
        """Suma valores de manera segura, ignorando None"""
        try:
            if attribute:
                total = 0
                for item in values:
                    if hasattr(item, attribute) or (isinstance(item, dict) and attribute in item):
                        value = getattr(item, attribute, None) if hasattr(item, attribute) else item.get(attribute)
                        if value is not None:
                            try:
                                total += float(value)
                            except (ValueError, TypeError):
                                continue
                return total
            else:
                total = 0
                for value in values:
                    if value is not None:
                        try:
                            total += float(value)
                        except (ValueError, TypeError):
                            continue
                return total
        except:
            return 0

    def safe_avg_filter(values, attribute=None):
        """Calcula promedio de manera segura, ignorando None"""
        try:
            if attribute:
                total = 0
                count = 0
                for item in values:
                    if hasattr(item, attribute) or (isinstance(item, dict) and attribute in item):
                        value = getattr(item, attribute, None) if hasattr(item, attribute) else item.get(attribute)
                        if value is not None:
                            try:
                                total += float(value)
                                count += 1
                            except (ValueError, TypeError):
                                continue
                return total / count if count > 0 else 0
            else:
                total = 0
                count = 0
                for value in values:
                    if value is not None:
                        try:
                            total += float(value)
                            count += 1
                        except (ValueError, TypeError):
                            continue
                return total / count if count > 0 else 0
        except:
            return 0

    def safe_count_filter(values, condition=None):
        """Cuenta valores de manera segura"""
        try:
            if condition is None:
                return sum(1 for v in values if v is not None)
            else:
                return sum(1 for v in values if v is not None and v == condition)
        except:
            return 0

    def count_true_attr_filter(values, attribute):
        """Cuenta objetos donde el atributo es True"""
        try:
            count = 0
            for item in values:
                if hasattr(item, attribute) or (isinstance(item, dict) and attribute in item):
                    value = getattr(item, attribute, None) if hasattr(item, attribute) else item.get(attribute)
                    if value:
                        count += 1
            return count
        except:
            return 0

    def safe_selectattr_filter(values, attribute):
        """Selecciona objetos con atributo no None"""
        try:
            result = []
            for item in values:
                if hasattr(item, attribute) or (isinstance(item, dict) and attribute in item):
                    value = getattr(item, attribute, None) if hasattr(item, attribute) else item.get(attribute)
                    if value is not None:
                        result.append(item)
            return result
        except:
            return []

    # Registrar filtros directamente
    app.jinja_env.filters['safe_sum'] = safe_sum_filter
    app.jinja_env.filters['safe_avg'] = safe_avg_filter
    app.jinja_env.filters['safe_count'] = safe_count_filter
    app.jinja_env.filters['count_true_attr'] = count_true_attr_filter
    app.jinja_env.filters['safe_selectattr'] = safe_selectattr_filter
    
    print("✅ Filtros registrados manualmente")
    
    return True

def verify_filters(app):
    """Verifica que todos los filtros estén registrados"""
    required_filters = ['safe_sum', 'safe_avg', 'safe_count', 'count_true_attr', 'safe_selectattr']
    
    missing_filters = []
    for filter_name in required_filters:
        if filter_name in app.jinja_env.filters:
            print(f"✅ Filtro '{filter_name}' registrado")
        else:
            print(f"❌ Filtro '{filter_name}' NO encontrado")
            missing_filters.append(filter_name)
    
    return len(missing_filters) == 0

def main():
    """Función principal"""
    print("🔧 CORRECTOR DE FILTROS DE JINJA2")
    print("=" * 50)
    
    try:
        # Importar la aplicación
        from app import app
        print("✅ Aplicación importada")
        
        # Verificar filtros actuales
        print("\n🔍 Verificando filtros actuales...")
        filters_ok = verify_filters(app)
        
        if not filters_ok:
            print("\n🔧 Registrando filtros manualmente...")
            register_filters_manually(app)
            
            print("\n🔍 Verificando filtros después del registro...")
            filters_ok = verify_filters(app)
        
        if filters_ok:
            print("\n🎉 ¡TODOS LOS FILTROS ESTÁN REGISTRADOS!")
            print("   Ahora puedes ejecutar: python run.py")
        else:
            print("\n❌ PROBLEMA PERSISTE")
            print("   Ejecuta: python reparar.py")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Ejecuta: python reparar.py")
    
    print("=" * 50)

if __name__ == "__main__":
    main()