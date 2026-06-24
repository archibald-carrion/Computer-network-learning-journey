import matplotlib.pyplot as plt
import shap

def shap_analysis(results, X_train_scaled, feature_names, label_encoder):
    """Run SHAP analysis for the trained Random Forest model."""
    print("\n--- SHAP Analysis for Random Forest ---")
    model = results['model']

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train_scaled[:1000])

    plt.figure(figsize=(12, 10))
    shap.summary_plot(
        shap_values,
        X_train_scaled[:1000],
        feature_names=feature_names,
        class_names=label_encoder.classes_,
        plot_type='bar',
        show=False,
        max_display=20,
    )
    plt.title('SHAP Feature Importance - Random Forest', fontsize=16)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig('shap_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(16, 12))
    shap.summary_plot(
        shap_values,
        X_train_scaled[:1000],
        feature_names=feature_names,
        class_names=label_encoder.classes_,
        show=False,
        max_display=20,
    )
    plt.title('SHAP Summary Plot - Random Forest', fontsize=16)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig('shap_summary_plot.png', dpi=300, bbox_inches='tight')
    plt.close()